import greek_features #seemingly unused here, but this makes the environment recognize features that are decorated
import os
import sys
from corpus_categories import composite_files, genre_to_files
from functools import reduce

from qcrit.color import RED, RESET
import qcrit.extract_features

from download_corpus import download_corpus

def main():
	#Validate command line options
	categories_to_include = set() if len(sys.argv) <= 2 else set(sys.argv[2:])
	if len(sys.argv) > 2 and not all(tok in genre_to_files for tok in categories_to_include):
		raise ValueError('Invalid genres: ' + str(categories_to_include - genre_to_files.keys()))

	corpus_path = ('tesserae', 'texts', 'grc')
	download_corpus(corpus_path)

	#Feature extractions
	qcrit.extract_features.main(
		os.path.join(*corpus_path), 

		'tess', 

		#Exclude all files of genres not specified. Exclude composite files no matter what
		excluded_paths=composite_files | (set() if len(sys.argv) <= 2 else 
			reduce(lambda cur_set, next_set: cur_set | next_set, 
			(genre_to_files[tok] for tok in genre_to_files if tok not in categories_to_include), set())),

		output_file=None if len(sys.argv) <= 1 else sys.argv[1] 
	)


if __name__ == '__main__':
	main()
