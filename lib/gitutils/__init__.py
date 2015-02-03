import os, subprocess
from threading import Thread

def _cd(dirpath):
  os.chdir(dirpath)

def _exec(cmd):
  s = subprocess.check_output(cmd)
  lines = s.split('\n')
  for l in lines:
    print(l)

def clone(dirpath, repo):
  _cd(dirpath)
  _exec(["git", "clone", repo])

def pull(dirpath):
  print ("PULLING: " + dirpath)
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
