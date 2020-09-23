import os
import re

while True:
	# kbd_input = os.read(0, 128).decode()
	# if len(kbd_input) == 0:
	# 	break
	# kbd_input_str = re.split("\\n", kbd_input)
	# kbd_input_arr = kbd_input.split("\\n")
	# kbd_input_arr = [item.split() for item in kbd_input_arr]
	# print(kbd_input_arr)


	kbd_input_str = input().strip() #input from the user
	kbd_input_arr = kbd_input_str.split() #parse to an array
	print(kbd_input_arr)
	for kbd_input_arr in kbd_input_arr:
		print(kbd_input_arr)






	# kbd_input_arr[-1] = kbd_input_arr[-1].splitlines()

	# kbd_input = kbd_input.decode()
	# if "\n" in kbd_input:
	# 	# kbd_input = kbd_input.rstrip("\n")
	# kbd_input = [item.strip() for item in kbd_input]
	# kbd_input_arr = [item.split() for item in kbd_input]
