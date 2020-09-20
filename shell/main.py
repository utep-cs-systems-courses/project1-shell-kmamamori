#!/usr/bin/env python3

import os
import sys
import re
import time

# receives string
def redirection(redirection_input):
    if '>' in redirection_input:
        redirection_input_arr = re.split('>|<', redirection_input)
        os.close(1)
        os.open(redirection_input_arr[1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)
    else:
        redirection_input_arr = re.split(' |>|<', redirection_input)
    args = redirection_input_arr[0].split()
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass
    os.write(
        2, ("Child:    Error: Could not exec %s.\n Command may not found.\n\n" % args[0]).encode())

# receives array
def changingDir(kbd_input_arr):
    try:
        os.chdir(kbd_input_arr[1])
    except:
        os.write(
            2, ("Something went wrong. Check the path you entered.\n").encode())
        pass

# recieve string
def check_command(cmd):
    if "cd" in cmd:
        changingDir(cmd.split(' '))
    else:
        redirection(cmd)


while True:
    if 'PS1' in os.environ: #if exist
        os.write(1, (os.environ['PS1']).encode())
    else:
        os.write(1, os.getcwd().encode())  # print prompt
    kbd_input_str = input(' $')  # get keyboard input
    kbd_input_arr = kbd_input_str.split(' ') #make str an array

    if 'exit' in kbd_input_arr:
        os.write(1, ("EXIT from Shell\n").encode())
        sys.exit(1)
    elif 'cd' in kbd_input_arr and not '|' in kbd_input_str:
        check_command(kbd_input_str)
    elif '|' in kbd_input_str:
        pipe_command = kbd_input_str.split('|')
        pr, pw = os.pipe()
        for f in (pr, pw):
            os.set_inheritable(f, True)
        pipe_rc = os.fork()
        if pipe_rc < 0:
            os.write(2, ("Fork failed!").encode())
            sys.exit(1)
        elif pipe_rc == 0: #child
            os.close(1) # close the output
            os.dup(pw)
            os.set_inheritable(1, True)
            for fd in (pr, pw):
                os.close(fd) #uneeded port
            check_command(pipe_command[0].strip())
        else: #parent
            os.close(0) #close input
            os.dup(pr)
            os.set_inheritable(0, True)  # set fd1 inheritable
            for fd in (pw, pr):
                os.close(fd) #uneeded port
            check_command(pipe_command[1].strip())
    else:
        pid = os.getpid()
        rc = os.fork()
        if rc < 0:
            # os.write(2, ("Fork failed!").encode())
            sys.exit(1)
        elif rc == 0:  # child
            if '/' in kbd_input_arr:
                program = kbd_input_arr[0]
                try:
                    os.execve(program, kbd_input_arr, os.environ)
                except FileNotFoundError:
                    pass
            elif '<' in kbd_input_arr or '>' in kbd_input_arr:
                redirection(kbd_input_str)
            else:
                redirection(kbd_input_str)
            sys.exit(1)
        else:  # parent
            if not '$' in kbd_input_str:
                childPidCode = os.wait()
