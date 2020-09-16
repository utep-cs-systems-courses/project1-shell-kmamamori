#! /usr/bin/python3

import os
import sys
import re
import time

"""
# 1. Prints a prompt string specified by shell variable PS1 when expecting a command (if PS1 is not set, the default prompt should be "$ ").
#
# 2. Accepts the standard unix command shell syntex for specifying commands and parameters
# 	* Your shell should create a child process that uses execve to run the command with its parameters.
# 	* If an absolute path is not specified, your shell should instead find it using the $PATH environment variable.
# 	* The parent process should wait for the child to terminate before printing another command prompt.
#
	# 3. Handles expected user error.
	# 	* Prints "command not found" if the command is not found. For example, if the user tries to run program `lx` and this program doesn't exist, the shell should respond with "lx: command not found".
	# 	* If the command fails (with a non-zero exit value N), your shell should print "Program terminated with exit code N."
#
# 4. Provides the following built-in commands.
* The "exit" command should cause your shell to terminate.
* Change directories with the "cd" command.
#
# 5. Redirection of input and output (e.g. $ ls > /tmp/files.txt).
#
# 6. Simple pipes (e.g. $ ls | sort -r).
#
	# 7. Background tasks (e.g. $ find /etc -print & )
"""

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
    if 'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
    else:
        os.write(1, os.getcwd().encode())  # print prompt
    kbd_input_str = input(' $')  # get keyboard input
    kbd_input_arr = kbd_input_str.split(' ')

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
        elif pipe_rc == 0:
            os.close(1)
            os.dup(pw)
            os.set_inheritable(1, True)
            for fd in (pr, pw):
                os.close(fd)
            check_command(pipe_command[0].strip())
        else:
            os.close(0)
            os.dup(pr)
            os.set_inheritable(0, True)  # set fd1 inheritable
            for fd in (pw, pr):
                os.close(fd)
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
