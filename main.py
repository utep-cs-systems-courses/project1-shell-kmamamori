import os
import sys
import re


"""
	# 1. Prints a prompt string specified by shell variable PS1 when expecting a command (if PS1 is not set, the default prompt should be "$ ").
"""
"""
	# 2. Accepts the standard unix command shell syntex for specifying commands and parameters
	# 	* Your shell should create a child process that uses execve to run the command with its parameters.
	# 	* If an absolute path is not specified, your shell should instead find it using the $PATH environment variable.
	# 	* The parent process should wait for the child to terminate before printing another command prompt.
"""
"""
	# 3. Handles expected user error.
	# 	* Prints "command not found" if the command is not found. For example, if the user tries to run program `lx` and this program doesn't exist, the shell should respond with "lx: command not found".
	# 	* If the command fails (with a non-zero exit value N), your shell should print "Program terminated with exit code N."
"""
"""
	# 4. Provides the following built-in commands.
	# 	* The "exit" command should cause your shell to terminate.
	# 	* Change directories with the "cd" command.
"""
"""
	# 5. Redirection of input and output (e.g. $ ls > /tmp/files.txt).
"""
"""
	# 6. Simple pipes (e.g. $ ls | sort -r).
"""
"""
	# 7. Background tasks (e.g. $ find /etc -print & )
"""


while True:
    os.write(1, os.getcwd().encode())  # print prompt
    kbd_input = input(' $')  # get keyboard input
    if (kbd_input == "exit"):
        os.write(1, ("Exit from Shell").encode())
        sys.exit(1)
    # print(kbd_input)  ## TEST
    rc = os.fork()
    # print(os.getpid()) ## TEST
