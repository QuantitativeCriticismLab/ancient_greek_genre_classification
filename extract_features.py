import os
import sys
import pickle
from color import RED, GREEN, RESET
from textual_feature import decorated_features

tesserae_clone_command = "git clone https://github.com/tesserae/tesserae.git"
greek_text_dir = "tesserae/texts/grc"

def __extract_features():
	text_to_features = {} #Associates file names to their respective features
	file_names = None

	#Download corpus if non-existent
	if not os.path.isdir(greek_text_dir):
		printa(RED + "Corpus at " + greek_text_dir + " does not exist - attempting to clone repository..." + RESET)
		os.system(tesserae_clone_command)

	#Obtain all the files to parse by traversing through the directory
	file_names = {current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in \
	os.walk(greek_text_dir) for current_file_name in current_file_names if current_file_name.endswith(".tess")}

	#Feature extraction
	for file_name in file_names:
		text_to_features[file_name] = {}

		#Store each line of file in a list
		file_text = []
		with open(file_name, mode="r", encoding="utf-8") as file:
			for line in file:
				#Ignore lines without tess tags, or parse the tag out and strip whitespace
				if not line.startswith("<"):
					continue
				assert ">" in line
				line = line[line.index(">") + 1:].strip()
				file_text.append(line)

		#Convert list of strings into a single string
		file_text = " ".join(file_text)

		#Default behavior is to invoke ALL decorated functions. If names of features are specified on the 
		#command line, then only invoke those
		for feature_name, func in decorated_features.items() if len(sys.argv) == 1 else \
		[(sys.argv[i], decorated_features[sys.argv[i]]) for i in range(1, len(sys.argv)) if sys.argv[i] in decorated_features]:
			score = func(file_text, file_name)
			text_to_features[file_name][feature_name] = score
			print(file_name + ", " + str(feature_name) + ", " + GREEN + str(score) + RESET)

	# with open("matrix.pickle", "wb") as pickle_file:
	# 	pickle_file.write(pickle.dumps(text_to_features))
	# 	pickle_file.close()

def main():
	from timeit import timeit
	print('\n\n' + GREEN + 'Elapsed time: ' + str(timeit(__extract_features, number=1)) + RESET)

