#! /usr/bin/env python3

import os, sys, time, re

def child(pid, argss):
   # print('\nA new child %d\n' %  os.getpid())
   # os._exit(0)  
   print (argss)
   #nw_dir = argss[1]
   if argss[0] == "cd":           #change directory
       print("changing dir...")
       os.chdir(argss[1])
       parent()
   else:
    print("trying exe: \n")
    os.execv('/bin/echo', ['foo', 'bar'])
    os.execv('/bin/cd', ['foo', 'try_dir'])
    
    os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
    args = ["wc", "p3-exec.py"]

    os.close(1)                 # redirect child's stdout
    sys.stdout = open("p4-output.txt", "w")
    os.set_inheritable(1, True)

    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, args[0])
        os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly 
    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error

def parent():
   while True:
      # newpid = os.fork()
      # #print("forked \n")
      # if newpid == 0:
         # child()
      # else:
         # pids = (os.getpid(), newpid)
         # print("parent: %d, child: %d\n" % pids)
      # reply = input("q for quit / c for new fork")
      # if reply == 'c': 
          # continue
      # else:
          # break
      inputt = ""
      pid = os.getpid()               # get and remember pid
      inputt = input(os.getcwd() + "$ ")
      argss = re.split('\s', inputt)  #get cmd args
      for a in argss:
          print (a)
      os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

      rc = os.fork()

      if rc < 0:
          os.write(2, ("fork failed, returning %d\n" % rc).encode())
          sys.exit(1)

      elif rc == 0:                   # child
          child(pid, argss)
          

      else:                           # parent (forked ok)
          os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
          
          childPidCode = os.wait()
          os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())
      
      #input = input("q for quit / c for new fork \n" + os.getcwd() + "$ " )
      if inputt == "exit": 
          print("Exiting shell...")
          sys.exit(1)
      else:
          continue

parent()
