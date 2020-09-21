#!/usr/bin/env python3

"""
    Name: Ken Amamori
    Course: Operatin System
    Professor: Eric Freudenthal 
    Lab: Shell Project with Python
"""

import os
import sys
import re

# receives arr to operate redirection ('<', '>')
def redirection(redirection_input):
    if '>' in redirection_input:
        os.close(1)
        os.open(redirection_input[redirection_input.index('>')+1], os.O_CREAT | os.O_WRONLY) #Create OR Write only
        os.set_inheritable(1, True)
        executingCommand(redirection_input[0:redirection_input.index('>')])
    else:
        os.close(0)
        os.open(redirection_input[redirection_input.index('<')+1], os.O_RDONLY) #Read only
        os.set_inheritable(0, True)
        executingCommand(redirection_input[0:redirection_input.index('<')])

# receives array and excuse 'ls' commands to change director
def changingDir(kbd_input_arr):
    try:
        os.chdir(kbd_input_arr[1])
    except FileNotFoundError:
        pass

# receives a array(kbd_input_arr) and executes pipe command
# Each commands are excuted on 'executingCommand' function
def pipe(kbd_input_arr):
    r_command = kbd_input_arr[kbd_input_arr.index('|')+1:] # split at('|')
    w_command = kbd_input_arr[0:kbd_input_arr.index('|')] # split 0~at('|')
    pr, pw = os.pipe() # Creates file descripter (r, w)
    for f in (pr, pw):
        os.set_inheritable(f, True)
    pipe_rc = os.fork() #fork for pipe command
    if pipe_rc < 0:
        os.write(2, ('Fork Failed.').encode())
        sys.exit(1)
    elif pipe_rc == 0:
        os.close(1)
        os.dup(pw)
        os.set_inheritable(1, True)
        for fd in (pr, pw):
            os.close(fd)
        executingCommand(w_command)
        sys.exit(1)
    else:
        os.close(0)
        os.dup(pr)
        os.set_inheritable(0, True)
        for fd in(pw, pr):
            os.close(fd) #closing
        if "|" in r_command: #check if another '|' character
            pipe(r_command) #recursive call in case of 2 pipes commands
        executingCommand(r_command)

# Receives a array (args) and excutes the command
def executingCommand(args):
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass
    os.write(2, ("Error: Command:'%s' not found." % args[0]).encode())
    sys.exit(1)

while True:
    p = os.getcwd()+' $' if 'PS1' not in os.environ else os.environ['PS1']
    os.write(1, p.encode())
    try:
        kbd_input_str = input().strip() #input from the user
        kbd_input_arr = kbd_input_str.split() #parse to an array
    except EOFError:
        sys.exit(1)
    if "exit" in kbd_input_arr: # user entered 'exit'
        sys.exit(0)
    isWaitSign = False if '&' in kbd_input_arr else True # value which deterines bg-'&' comparison at the end
    if not isWaitSign:
        kbd_input_arr.remove('&')
    if len(kbd_input_arr) <= 0:
        continue
    if kbd_input_arr[0] == 'cd': #directory change command
        changingDir(kbd_input_arr)
    elif '|' in kbd_input_arr: # pipe command
        pipe(kbd_input_arr)
    else:
        rc = os.fork()
        if rc < 0:
            os.write(2, ("Fork Failed.\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            if '/' in kbd_input_arr[0]:
                try:
                    os.execve(kbd_input_arr[0], kbd_input_arr, os.environ)
                except FileNotFoundError:
                    pass
            elif '>' in kbd_input_arr or '<' in kbd_input_arr: # Redirection
                redirection(kbd_input_arr)
            else:
                for dir in re.split(":", os.environ['PATH']):
                    program = "%s/%s" % (dir, kbd_input_arr[0])
                    try:
                        os.execve(program, kbd_input_arr, os.environ)
                    except FileNotFoundError:
                        pass
        else:
            if isWaitSign:
                os.wait()