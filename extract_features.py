import os
import pickle
from color import RED, GREEN, RESET
from textual_feature import decorated_features

def parse_tess(file_name):
	from io import StringIO
	file_text = StringIO()
	with open(file_name, mode='r', encoding='utf-8') as file:
		for line in file:
			#Ignore lines without tess tags, or parse the tag out and strip whitespace
			if not line.startswith('<'):
				continue
			assert '>' in line
			file_text.write(line[line.index('>') + 1:].strip())
			file_text.write(' ')
	return file_text.getvalue()

file_parsers = {\
	'tess': parse_tess, \
}

def __extract_features(corpus_dir, file_extension, features):
	text_to_features = {} #Associates file names to their respective features
	file_names = None

	#Obtain all the files to parse by traversing through the directory
	file_names = sorted(list({current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in \
	os.walk(corpus_dir) for current_file_name in current_file_names if current_file_name.endswith('.' + file_extension)}))
	feature_tuples = [(name, decorated_features[name]) for name in features]

	#Feature extraction
	for file_name in file_names:
		text_to_features[file_name] = {}

		file_text = file_parsers[file_extension](file_name)

		for feature_name, func in feature_tuples:
			score = func(file_text, file_name)
			text_to_features[file_name][feature_name] = score
			print(file_name + ', ' + str(feature_name) + ', ' + GREEN + str(score) + RESET)

	# with open('matrix.pickle', 'wb') as pickle_file:
	# 	pickle_file.write(pickle.dumps(text_to_features))
	# 	pickle_file.close()

def main(corpus_dir, file_extension, features=None):
	if features is None:
		features = decorated_features.keys()
	assert corpus_dir and file_extension and features, \
		'Parameters must not be "None"'
	assert os.path.isdir(corpus_dir), \
		'Path "' + corpus_dir + '" is not a valid directory'
	assert file_extension in file_parsers, \
		'"' + str(file_extension) + '" is not an available file extension to parse'
	assert all(name in decorated_features.keys() for name in features), \
		'Features names must be among ' + str(decorated_features.keys())
	from timeit import timeit
	from functools import partial
	print('\n\n' + GREEN + 'Elapsed time: ' + \
		str(timeit(partial(__extract_features, corpus_dir, file_extension, features), number=1)) + RESET)
