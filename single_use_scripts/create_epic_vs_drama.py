output_filename = 'labels/one_vs_one/drama_vs_epic.csv'
output_file = open(output_filename, 'w')
output_file.write('drama:0,epic:1\nFilename,Genre\n')

input_file = open('labels/genre_labels.csv')
input_file.readline()
input_file.readline()

for line in input_file:
	arr = line.strip().split(',')
	if arr[1] == '6':
		output_file.write(arr[0] + ',0\n')
	elif arr[1] == '7':
		output_file.write(arr[0] + ',1\n')
print('Success!')