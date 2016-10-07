import cherrypy, locations, os 
from processpipe import Process, ProcessException


class LocalFileProcess(Process):

  def __init__(self, filepath):
    Process.__init__(self)
    self.filepath = filepath

  def name(self):
    return 'localfile'

  def start(self, args):
    self.args = {}
    self.args['outfile'] = self.filepath
    self.msg_ready(self.args)

  def stop(self):
    self.msg_finished()
