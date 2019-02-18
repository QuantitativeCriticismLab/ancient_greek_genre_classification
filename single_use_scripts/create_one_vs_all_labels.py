#Uncomment one of these options
#------ Greek prose
# labels = {'prose_miscellaneous': '0', 'letters': '1', 'technical_treatise': '2', 'oratory': '3', 'history': '4', 'philosophy': '5'}
# category = 'prose'
# input_filename = 'labels/genre_labels.csv'
# output_dir = 'labels/one_vs_all_in_same_genre/'
#------ Greek verse
# labels = {'drama': '6', 'epic': '7', 'verse_miscellaneous': '8'}
# category = 'verse'
# input_filename = 'labels/genre_labels.csv'
# output_dir = 'labels/one_vs_all_in_same_genre/'
#------ Latin prose
# labels = {'history': '0', 'oratory': '1', 'miscellaneous': '2', 'letters': '3', 'technical_treatise': '4', 'philosophy': '5'}
# category = 'prose'
# input_filename = 'latin/labels/prose_labels.csv'
# output_dir = 'latin/labels/one_vs_all_in_same_genre/'
#------ Latin verse
# labels = {'miscellaneous': '0', 'elegy': '1', 'epic': '2', 'drama': '3'}
# category = 'verse'
# input_filename = 'latin/labels/verse_labels.csv'
# output_dir = 'latin/labels/one_vs_all_in_same_genre/'

for k, v in labels.items():
	output_filename = output_dir + k + '_vs_rest_of_' + category + '.csv'
	output_file = open(output_filename, 'w')

	output_file.write(k + ':0,' + '_or_'.join(ke for ke in labels if ke != k) + ':1\n')

	output_file.write('Text_Name,Genre\n')

	input_file = open(input_filename)

	input_file.readline()
	input_file.readline()

	for line in input_file:
		arr = line.strip().split(',')
		if arr[1] == v:
			output_file.write(arr[0] + ',0\n')
		elif arr[1] in labels.values():
			output_file.write(arr[0] + ',1\n')

print('Success!')
