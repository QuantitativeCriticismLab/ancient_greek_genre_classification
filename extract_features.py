import os
import sys
import pickle
import functools
from color import RED, GREEN, RESET
from textual_feature import decorated_features

def parse_tess(file_name):
	file_text = []
	with open(file_name, mode='r', encoding='utf-8') as file:
		for line in file:
			#Ignore lines without tess tags, or parse the tag out and strip whitespace
			if not line.startswith('<'):
				continue
			assert '>' in line
			line = line[line.index('>') + 1:].strip()
			file_text.append(line)
	return ' '.join(file_text)

file_parsers = {\
	'tess': parse_tess, \
}

def __extract_features(corpus_dir, file_extension):
	assert file_extension in file_parsers, '"' + str(file_extension) + '" is not an available file extension to parse'
	text_to_features = {} #Associates file names to their respective features
	file_names = None

	#Obtain all the files to parse by traversing through the directory
	file_names = {current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in \
	os.walk(corpus_dir) for current_file_name in current_file_names if current_file_name.endswith('.' + file_extension)}

	#Feature extraction
	for file_name in file_names:
		text_to_features[file_name] = {}

		file_text = file_parsers[file_extension](file_name)

		#Default behavior is to invoke ALL decorated functions. If names of features are specified on the 
		#command line, then only invoke those
		for feature_name, func in decorated_features.items() if len(sys.argv) == 1 else \
		[(sys.argv[i], decorated_features[sys.argv[i]]) for i in range(1, len(sys.argv)) if sys.argv[i] in decorated_features]:
			score = func(file_text, file_name)
			text_to_features[file_name][feature_name] = score
			print(file_name + ', ' + str(feature_name) + ', ' + GREEN + str(score) + RESET)

	# with open('matrix.pickle', 'wb') as pickle_file:
	# 	pickle_file.write(pickle.dumps(text_to_features))
	# 	pickle_file.close()

def main(corpus_dir, file_extension):
	from timeit import timeit
	print('\n\n' + GREEN + 'Elapsed time: ' + \
		str(timeit(functools.partial(__extract_features, corpus_dir, file_extension), number=1)) + RESET)
