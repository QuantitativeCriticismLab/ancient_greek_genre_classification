#pylint: disable = C0330
'''Run feature extraction'''
import os
import sys
from functools import reduce

import qcrit.extract_features
from qcrit.textual_feature import setup_tokenizers

from download_corpus import download_corpus
from corpus_categories import composite_files, genre_to_files

def main():
	'''Main'''
	corpus_path = ('tesserae', 'texts', 'grc')
	download_corpus(corpus_path)

	#'FULL STOP', 'SEMICOLON', 'GREEK QUESTION MARK'
	setup_tokenizers(terminal_punctuation=('.', ';', ';'))

	if len(sys.argv) > 2 and sys.argv[2] == '-u':
		import qcrit.features.universal_features #seemingly unused, but allows the recognition of features
	else:
		import qcrit.features.ancient_greek_features #seemingly unused, but allows the recognition of features

	#Feature extractions
	qcrit.extract_features.main(
		os.path.join(*corpus_path),

		{'tess': qcrit.extract_features.parse_tess},

		#Exclude all files of genres not specified. Exclude composite files no matter what
		excluded_paths=composite_files,

		output_file=None if len(sys.argv) <= 1 else sys.argv[1]
	)

if __name__ == '__main__':
	main()
