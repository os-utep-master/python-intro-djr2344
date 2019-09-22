#! /usr/bin/env python3

import os, sys, time, re

def child(pid, cmd, argss):  
   print ("command is: " + str(argss))
   os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
   #deal with pipes --------------------------------------------------
   if "|" in argss:           
    stp = argss.index("|")
    #print (stp)
    frst_args = [] # the command before the first pipe
    scnd_args = [] # the command after the first pipe
    i = 0
    for a in argss:
        if i < stp:
            if argss.index(a) < stp:
                frst_args.append(a)    #grab the command before "|" 
        elif i > stp:
                scnd_args.append(a)   #grab the command after "|"
        i = i + 1
    print ("first command to be executed: " + str(frst_args))
    fcmd = ""
    for c in frst_args:
        fcmd = fcmd + c
    print ("second command to be executed: " + str(scnd_args))
    pid = os.getpid()               # get and remember pid
    
    #pipe stuff
    pr,pw = os.pipe()
    for f in (pr, pw):
        os.set_inheritable(f, True)
    print("pipe fds: pr=%d, pw=%d" % (pr, pw))
    import fileinput
    
    os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

    rc = os.fork()

    if rc < 0:
          os.write(2, ("fork failed, returning %d\n" % rc).encode())
          sys.exit(1)

    elif rc == 0:                   # child
          print("Child: My pid==%d.  Parent's pid=%d" % (os.getpid(), pid), file=sys.stderr)
          os.close(1)                 # redirect child's stdout
          os.dup(pw)
          
          for fd in (pr, pw):
            os.close(fd)
          child(pid, fcmd, frst_args)
          
    else:                           # parent (forked ok)
          print("Parent: My pid==%d.  Child's pid=%d" % (os.getpid(), rc), file=sys.stderr)
          os.close(0)
          os.dup(pr)
          for fd in (pw, pr):
              os.close(fd)
          for line in fileinput.input():
              print("From child: <%s> \n" % line)

#----------------------------------------------------------------------------------------------------   
   elif argss[0] == "cd":           #change directory
       print("changing dir...")
       os.chdir(argss[1])
       parent()
       sys.exit(1)

   elif argss[0] == "ls":    #list directory
     print("trying ls : \n")
     if ">" in argss :        #redirect output
        print("redirecting output... \n")
        sp = argss.index(">")
        nw_args = []
        i = 0
        outp = ""
        for a in argss:
            if argss.index(a) < sp:
                nw_args.append(a)    #grab the command before ">" 
            elif argss.index(a) > sp:
                outp = a   #grab where the output is to be redirected
            i = i + 1
        print ("command to be executed: " + str(nw_args))
        print ("redirected output to: " + outp)
        os.close(1)
        sys.stdout = open(outp, "w")
        os.set_inheritable(1, True)
        for dir in re.split(":", os.environ['PATH']): # try each directory in path
         program = "%s/%s" % (dir, nw_args[0])
         os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
         try:
             #print (os.environ)
             os.execve(program, nw_args, os.environ) # try to exec program
         except FileNotFoundError:             # ...expected
             pass                              # ...fail quietly 
        os.write(2, ("Child:    Error: Could not exec %s\n" % nw_args[0]).encode())
        sys.exit(1)                 # terminate with error
        
     else:
        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, argss[0])
            os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
            try:
                #print (os.environ)
                os.execve(program, argss, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly 
        os.write(2, ("Child:    Error: Could not exec %s\n" % argss[0]).encode())
        sys.exit(1)                 # terminate with error
   else:
    print("attempting last resort... \n")
    os.system(cmd)

def parent():
   while True:
      inputt = ""
      pid = os.getpid()               # get and remember pid
      inputt = input(os.getcwd() + "$ ")
      argss = re.split('\s', inputt)  #get cmd args
      #for a in argss:
      #    print (a)
      os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

      rc = os.fork()

      if rc < 0:
          os.write(2, ("fork failed, returning %d\n" % rc).encode())
          sys.exit(1)

      elif rc == 0:                   # child
          child(pid, inputt, argss)
          

      else:                           # parent (forked ok)
          os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
          
          childPidCode = os.wait()
          os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())
      if inputt == "exit": 
          print("Exiting shell...")
          sys.exit(1)
      else:
          continue

parent()
