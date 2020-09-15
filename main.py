import os
import sys
import re


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
	# 	* The "exit" command should cause your shell to terminate.
	# 	* Change directories with the "cd" command.
#
	# 5. Redirection of input and output (e.g. $ ls > /tmp/files.txt).
#
	# 6. Simple pipes (e.g. $ ls | sort -r).
#
	# 7. Background tasks (e.g. $ find /etc -print & )
"""


while True:
    os.write(1, os.getcwd().encode())  # print prompt
    kbd_input = input(' $').split(' ')  # get keyboard input

    if 'exit' in kbd_input:
        os.write(1, ("EXIT from Shell\n").encode())
        sys.exit(1)
    elif 'cd' in kbd_input:
        print("\n"+kbd_input[1]+"\n")
        try:
            os.chdir(kbd_input[1])
            # os.write(1, (os.getcwd()).encode())
        except:
            os.write(2, ("Something went wrong. Check the path you entered.\n").encode())
            pass

    else:
        rc = os.fork()
        if rc < 0:
            os.write(2, ("Fork failed!").encode())
            sys.exit(1)
        elif rc == 0: # child
            os.write(1, ("Successful forked").encode())
            sys.exit(1)
        else: # parent
            os.write(1, ("Parent!").encode())
            childPidCode = os.wait()
            os.write(1, ("The child will terminate with this").encode())
            os.wait()

    # print(kbd_input)  ## TEST
    # rc = os.fork()
    # print(os.getpid()) ## TEST