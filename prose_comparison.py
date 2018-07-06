names_from_author_labels = set()
names_from_prose_list = set()

f = open('author_labels.txt')
for line in f:
	line = line.strip()
	if line.endswith('p'):
		names_from_author_labels.add(line.split(' - ')[0].replace(' ', '_').lower())
f = open('tesserae/texts/prose_list')
for line in f:
	if line == '# greek\n':
		break
for line in f:
	line = line.replace('\\', '').replace('.', '').replace('\n', '')
	names_from_prose_list.add(line)
print(names_from_author_labels)
print(names_from_prose_list)
print()
print(names_from_author_labels - names_from_prose_list)
print(names_from_prose_list - names_from_author_labels)
