#Uncomment one of these two options
#------
labels = {'prose_miscellaneous': '0', 'letters': '1', 'technical_treatise': '2', 'oratory': '3', 'history': '4', 'philosophy': '5'}
category = 'prose'
#------
# labels = {'drama': '6', 'epic': '7', 'verse_miscellaneous': '8'}
# category = 'verse'
#------

for k, v in labels.items():
	output_file_name = k + '_vs_rest_of_' + category + '.csv'
	output_file = open(output_file_name, 'w')

	output_file.write(k + ':0,' + '_or_'.join(ke for ke in labels if ke != k) + ':1\n')

	output_file.write('Filename,Genre\n')

	input_file = open('labels/genre_labels.csv')

	input_file.readline()
	input_file.readline()

	for line in input_file:
		arr = line.strip().split(',')
		if arr[1] == v:
			output_file.write(arr[0] + ',0\n')
		elif arr[1] in labels.values():
			output_file.write(arr[0] + ',1\n')

print('Success!')
