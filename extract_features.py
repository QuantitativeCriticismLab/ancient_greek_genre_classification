import sys
import pickle
import os
from os.path import join
from color import RED, GREEN, YELLOW, RESET
from textual_feature import decorated_features, clear_cache, tokenize_types, debug_output
from progress_bar import print_progress_bar
from io import StringIO

def parse_tess(file_name):
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

file_parsers = {
	'tess': parse_tess, 
}

def _extract_features(corpus_dir, file_extension, features, output_file):
	text_to_features = {} #Associates file names to their respective features
	file_names = None

	#Obtain all the files to parse by traversing through the directory
	file_names = sorted(list({join(current_path, current_file_name) for current_path, current_dir_names, current_file_names in 
	os.walk(corpus_dir) for current_file_name in current_file_names if current_file_name.endswith('.' + file_extension)}))
	feature_tuples = [(name, decorated_features[name]) for name in features]

	print('Extracting features from ' + YELLOW + join(corpus_dir, '*.' + file_extension) + RESET)

	#Feature extraction
	file_no = 1
	for file_name in file_names:
		text_to_features[file_name] = {}

		file_text = file_parsers[file_extension](file_name)

		for feature_name, func in feature_tuples:
			score = func(file_text, file_name)
			text_to_features[file_name][feature_name] = score
			if output_file is None:
				print(file_name + ', ' + str(feature_name) + ', ' + GREEN + str(score) + RESET)

		if output_file is not None:
			print_progress_bar(file_no, len(file_names), prefix='Progress', 
				suffix='(%d of %d files)' % (file_no, len(file_names)), length=43)
			file_no += 1

	clear_cache(tokenize_types, debug_output)

	if output_file is not None:
		print('Feature mining complete. Attempting to write feature results to "' + YELLOW + output_file + RESET + '"...')
		with open(output_file, 'wb') as pickle_file:
			pickle_file.write(pickle.dumps(text_to_features))
		print(GREEN + 'Success!' + RESET)

def main(corpus_dir, file_extension, features=None, output_file=None):
	if features is None:
		features = decorated_features.keys()
	assert corpus_dir and file_extension and features, \
		'Parameters must be truthy'
	assert os.path.isdir(corpus_dir), \
		'Path "' + corpus_dir + '" is not a valid directory'
	assert file_extension in file_parsers, \
		'"' + str(file_extension) + '" is not an available file extension to parse'
	assert all(name in decorated_features.keys() for name in features), \
		'Features names must be among ' + str(decorated_features.keys())
	assert output_file is None or (output_file and type(output_file) is str and not os.path.isfile(output_file)), \
		'Output file "' + output_file + '" is invalid or already exists!'
	from timeit import timeit
	from functools import partial
	print('\n\n' + GREEN + 'Elapsed time: ' + \
		str(timeit(partial(_extract_features, corpus_dir, file_extension, features, output_file), number=1)) + RESET)
