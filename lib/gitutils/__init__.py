import os, subprocess, cherrypy
from threading import Thread

def _cd(dirpath):
  os.chdir(dirpath)

def _exec(cmd):
  s = subprocess.check_output(cmd)
  lines = s.split('\n')
  for l in lines:
    if l.strip() != "":
      cherrypy.log("GIT: " + l)

def clone(dirpath, repo):
  _cd(dirpath)
  _exec(["git", "clone", repo])

def pull(dirpath):
  if not os.path.exists(os.path.join(dirpath, ".git")):
    return
  cherrypy.log("GIT: pulling " + dirpath)
  _cd(dirpath)
  _exec(["git", "pull"])

def pull_subdirs(dirpath):
  dirs = os.listdir(dirpath)
  threads = []
  for d in dirs:
    th = Thread(target=pull, args=(os.path.join(dirpath, d),))
    th.start()
    threads.append(th)

  for thread in threads:
    thread.join()
