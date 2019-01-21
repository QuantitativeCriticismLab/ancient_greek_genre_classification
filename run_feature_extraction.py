import greek_features #seemingly unused here, but this makes the environment recognize features that are decorated
import extract_features
import os
import sys
from corpus_categories import composite_files, genre_to_files
from functools import reduce
from color import RED, RESET

if __name__ == '__main__':

	#Validate command line options
	categories_to_include = set() if len(sys.argv) <= 2 else set(sys.argv[2:])
	if len(sys.argv) > 2 and not all(tok in genre_to_files for tok in categories_to_include):
		raise ValueError('Invalid genres: ' + str(categories_to_include - genre_to_files.keys()))

	#Download corpus if non-existent
	corpus_dir = os.path.join('tesserae', 'texts', 'grc')
	tesserae_clone_command = 'git clone https://github.com/timgianitsos/tesserae.git'
	if not os.path.isdir(corpus_dir):
		print(RED + 'Corpus at ' + corpus_dir + ' does not exist - attempting to clone repository...' + RESET)
		if os.system(tesserae_clone_command) is not 0:
			raise Exception('Unable to obtain corpus for feature extraction')

	#Feature extractions
	extract_features.main(
		corpus_dir, 

		'tess', 

		#Exclude all files of genres not specified. Exclude composite files no matter what
		excluded_paths=composite_files | (set() if len(sys.argv) <= 2 else 
			reduce(lambda cur_set, next_set: cur_set | next_set, 
			(genre_to_files[tok] for tok in genre_to_files if tok not in categories_to_include), set())),

		output_file=None if len(sys.argv) <= 1 else sys.argv[1] 
	)
