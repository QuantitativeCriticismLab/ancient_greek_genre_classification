classification_file = open('classifications.csv')
new_class_file = open('new_class.csv', mode='w')
new_class_file.write(classification_file.readline())
for line in classification_file:
	line = line.strip().split(',')
	new_class_file.write(line[0] + ',')
	new_class_file.write(('1' if line[1] == 'True' else '0') + '\n')
