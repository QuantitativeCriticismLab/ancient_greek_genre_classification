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

def _get_filenames(corpus_dir, file_extension, excluded_paths):
	#Obtain all the files to parse by traversing through the corpus directory
	file_names = []
	for current_path, current_dir_names, current_file_names in os.walk(corpus_dir, topdown=True):
		
		#Remove the excluded directories to prevent traversing into them
		del_indexes = []
		for i, d in enumerate(current_dir_names):
			if (join(current_path, d) + os.sep) in excluded_paths:
				del_indexes.append(i)
		#Iterate backwards to prevent index removal issues
		for i in range(len(del_indexes) - 1, -1, -1):
			del current_dir_names[del_indexes[i]]

		for current_file_name in current_file_names:
			if current_file_name.endswith('.' + file_extension) \
			and join(current_path, current_file_name) not in excluded_paths:
				file_names.append(join(current_path, current_file_name))
	return sorted(file_names)

def _extract_features(corpus_dir, file_extension, excluded_paths, features, output_file):
	file_names = _get_filenames(corpus_dir, file_extension, excluded_paths)
	feature_tuples = [(name, decorated_features[name]) for name in features]
	text_to_features = {} #Associates file names to their respective features
	print('Extracting features from .' + file_extension + ' files in ' + YELLOW + corpus_dir + RESET)

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

# file_extension must not include the dot ('.')
# If excluded_paths is given, it must be a set and it can contain files or directories (the directories must 
# end in a file separator e.g. slash on Mac or Linux and backslash on Windows)
def main(corpus_dir, file_extension, excluded_paths=None, features=None, output_file=None):
	if features is None:
		features = decorated_features.keys()
	if excluded_paths is None:
		excluded_paths = set()
	assert corpus_dir and file_extension and features, \
		'Parameters must be truthy'
	assert os.path.isdir(corpus_dir), \
		'Path "' + corpus_dir + '" is not a valid directory'
	assert file_extension in file_parsers, \
		'"' + str(file_extension) + '" is not an available file extension to parse'
	assert not excluded_paths or all(os.path.isfile(path) or os.path.isdir(path) for path in excluded_paths), \
		'Each path in ' + str(excluded_paths) + ' must be a valid path for a file or directory!'
	assert all(name in decorated_features.keys() for name in features), \
		'Features names must be among ' + str(decorated_features.keys())
	assert output_file is None or (output_file and type(output_file) is str and not os.path.isfile(output_file)), \
		'Output file "' + output_file + '" is invalid or already exists!'
	from timeit import timeit
	from functools import partial
	print(
		'\n\n' + GREEN + 'Elapsed time: ' + str(timeit(
		partial(_extract_features, corpus_dir, file_extension, excluded_paths, features, output_file), number=1)) + 
		' seconds' + RESET
	)
