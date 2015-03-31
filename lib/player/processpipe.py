from Queue import Queue
from threading import Thread
import subprocess32 as subprocess
import os, select, signal, cherrypy, shutil

MSG_PROCESS_READY = 1
MSG_PROCESS_HALTED = 2
MSG_PROCESS_FINISHED = 3

MSG_PLAYER_PIPE_STOPPED = 4

TMP_DIR = "/tmp/blissflixx"
OUT_FILE = "/tmp/blissflixx/bf.out"

def _start_thread(target, *args):
  th = Thread(target=target, args=args)
  th.daemon = True
  th.start()
  return th

class _DiscardFile(object):
  def write(self, *args):
    pass
  def close(self):
    pass

def _copypipe(src, dest):
  if not dest:
    dest = _DiscardFile()

  # Ignore broken pipe errors if process
  # are forced to stop
  try:
    shutil.copyfileobj(src, dest)
  except Exception:
    pass

  src.close()
  dest.close()

def _bgcopypipe(src, dest):
  return _start_thread(_copypipe, src, dest)

class ProcessException(Exception):
  pass

class ProcessPipe(object):

  def __init__(self, title):
    self.title = title
    self.procs = []
    self.threads = []
    self.msgq = Queue()
    self.next_proc = 0
    self.stopping = False
    self.started = False

  def status_msg(self):
    if self.started:
      return self.title
    else:
      idx = self.next_proc - 1
      if idx < 0:
        idx = 0
      return self.procs[idx].status_msg()

  def add_process(self, proc):
    self.procs.append(proc)

  def start(self, pmsgq):
    self.pmsgq = pmsgq
    self._start_next()
    while True:
      m = self.msgq.get()
      idx = self.msgq.get()
      name = self.procs[idx].name()

      if m == MSG_PROCESS_READY:
        cherrypy.log("READY: " + name)
        args = self.msgq.get()
        if not self._is_last_proc(idx):
          self._start_next(args)
        else:
          self.started = True

      elif m == MSG_PROCESS_FINISHED:
        cherrypy.log("FINISHED: " + name)
        if self._is_last_proc(idx):
          self.stop()
          break

      elif m == MSG_PROCESS_HALTED:
        cherrypy.log("HALTED: " + name)
        self.stop()
        break

  def _is_last_proc(self, idx):
    return idx == len(self.procs) - 1

  def _start_next(self, args={}):
    proc = self.procs[self.next_proc]
    cherrypy.log("STARTING: " + proc.name())
    proc.set_msgq(self.msgq, self.next_proc)
    self.threads.append(_start_thread(proc.start, args))
    self.next_proc = self.next_proc + 1

  def stop(self):
    if self.stopping:
      return
    self.stopping = True
    self.started = False
    error = None
    for idx in xrange(self.next_proc-1, -1, -1):
      proc = self.procs[idx]
      proc.stop()
      self.threads[idx].join()
      if proc.has_error(): 
        error = proc.get_errors()[0]
        cherrypy.log("GOT ERROR: " + error)
    self.pmsgq.put(MSG_PLAYER_PIPE_STOPPED)
    self.pmsgq.put(error)

  def is_started(self):
    return self.started

class Process(object):

  def __init__(self):
    self.errors = []

  def set_msgq(self, msgq, procidx):
    self.msgq = msgq
    self.procidx = procidx

  def _send(self, msg, args=None):
    self.msgq.put(msg)
    self.msgq.put(self.procidx)
    if args is not None:
      self.msgq.put(args)

  def _set_error(self, msg):
    self.errors.append(msg)

  def get_errors(self):
    return self.errors

  def has_error(self):
    return len(self.errors) > 0

  def status_msg(self):
    return "LOADING STREAM"

  def name(self):
    raise NotImplementedError('This method must be implemented by subclasses') 

  def start(self, args):
    raise NotImplementedError('This method must be implemented by subclasses') 

  def stop(self):
    raise NotImplementedError('This method must be implemented by subclasses') 

  def msg_ready(self, args=None):
    if args is None:
      args = {}
    self._send(MSG_PROCESS_READY, args)

  def msg_halted(self):
    self._send(MSG_PROCESS_HALTED)

  def msg_finished(self):
    self._send(MSG_PROCESS_FINISHED)

class ExternalProcess(Process):

  def __init__(self, shell=False):
    Process.__init__(self)
    self.shell = shell
    self.killing = False
    if not os.path.exists(TMP_DIR):
      os.makedirs(TMP_DIR)

  def start(self, args):
    cmd = self._get_cmd(args)
    self.proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT, 
                                 stdout=subprocess.PIPE, preexec_fn=os.setsid,
                                 shell=self.shell)
    try:
      args = self._ready() 
      self.msg_ready(args)
    except ProcessException, e:
      # Ignore errors if process is being killed
      if not self.killing:
        self._set_error(str(e))

    self._wait()

  def _wait(self):
    # Drain stderr/stdout pipe to stop it filling up and blocking process
    cpthr = _bgcopypipe(self.proc.stdout, None)
    retcode = self.proc.wait()
    self.proc = None

    #if retcode != 0:
    #  cherrypy.log("Process exited with code: " + str(retcode))
    if self.has_error() or self.killing:
      self.msg_halted()
    else:
      self.msg_finished()
      
  def stop(self):
    if self.proc is not None:
      # Stop gets called from a seperate thread 
      # so shutdown may already be in progress
      # when we try to kill - therefore ignore errors
      try:
        # kill - including all children of process
        self.killing = True
        os.killpg(self.proc.pid, signal.SIGKILL)
      except Exception, e:
        pass

    if os.path.exists(OUT_FILE):
      try:
        os.remove(OUT_FILE)
      except Exception:
        pass

  def _get_cmd(self):
    raise NotImplementedError('This method must be implemented by subclasses') 

  def _ready(self):
    raise NotImplementedError('This method must be implemented by subclasses') 

  def _readline(self, timeout=None):
    poll_obj = select.poll()
    poll_obj.register(self.proc.stdout, select.POLLIN)
    while self.proc.poll() is None:
      if timeout is not None:
        poll_result = poll_obj.poll(1000 * timeout)
        if not poll_result:
          raise ProcessException("Timed out waiting for input")
      line = self.proc.stdout.readline()
      if not line:
        raise ProcessException("Process suddenly died")
      line = line.strip()
      if line.strip() != '':
        return line
    return None

