# # From https://stackoverflow.com/a/34325723

# # Print iterations progress
def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
	"""
	Call in a loop to create terminal progress bar
	@params:
	    iteration   - Required  : current iteration (Int)
	    total       - Required  : total iterations (Int)
	    prefix      - Optional  : prefix string (Str)
	    suffix      - Optional  : suffix string (Str)
	    decimals    - Optional  : positive number of decimals in percent complete (Int)
	    length      - Optional  : character length of bar (Int)
	    fill        - Optional  : bar fill character (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
	

	# Print New Line on Complete
	if iteration == total: 
		print()

if __name__ == '__main__':
	# 
	# Sample Usage
	# 

	# https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python
	import os
	# columns is width of window printing progress bar
	rows, columns = os.popen('stty size', 'r').read().split()

	from time import sleep

	# A List of Items
	items = list(range(0, 57))
	l = len(items)	#57
	barLen = int(columns) - 27 # prefix, bar, percent, suffix are 27 spaces

	#if bar length is too small, don't print bar
	if barLen >= 0:
		# Initial call to print 0% progress
		print_progress_bar(0, l, prefix = 'Progress:', suffix = 'Complete', length = barLen)
		for i, item in enumerate(items):
			# Do stuff...
			sleep(0.1)
			# Update Progress bar

			#import shutil; shutil.get_terminal_size()
			#columns

			print_progress_bar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = barLen)


	else :
		print("Window size too small to show progress bar")









