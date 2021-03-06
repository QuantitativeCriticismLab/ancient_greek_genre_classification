import os
from os.path import join
from collections import OrderedDict

#Take author labels and assign them to each file by that author

tesserae_clone_command = "git clone https://github.com/timgianitsos/tesserae.git"
greek_text_dir = "tesserae/texts/grc"

author_to_isprose = {}
with open("author_labels.txt", mode="r") as file:
	for line in file:
		line = line.strip().split(" - ")
		assert line[1] == 'p' or line[1] == 'v'
		author_to_isprose[line[0].lower().replace(' ', '_')] = 1 if line[1] == 'p' else 0

#Download corpus if non-existent
if not os.path.isdir(greek_text_dir):
	print("Corpus at " + greek_text_dir + " does not exist - attempting to clone repository...")
	os.system(tesserae_clone_command)

file_names = sorted([join(current_path, current_file_name) for current_path, current_dir_names, current_file_names in \
os.walk(greek_text_dir) for current_file_name in current_file_names if current_file_name.endswith(".tess")])

file_to_isprose = OrderedDict()

for file in file_names:
	index_of_filename = file.rindex(os.sep) + 1
	author = file[index_of_filename: file.index('.', index_of_filename)]
	isprose = author_to_isprose[author]
	file_to_isprose[file] = isprose

with open("prosody_labels.csv", mode="w") as file:
	file.write("verse:0,prose:1\n")
	file.write("Filename,Label\n")
	for k, v in file_to_isprose.items():
		file.write(k + ',' + str(v) + '\n')

print("Complete!")
