import greek_features #seemingly unused here, but this makes the environment recognize features
import extract_features
from corpus_categories import composite_files, verse_misc_files, prose_files
import os
import sys

if __name__ == '__main__':

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

		#Exclude the following directories and files
		excluded_paths=composite_files | verse_misc_files | prose_files,

		#Output the results to a file to be processed by machine learning algorithms
		output_file=None if len(sys.argv) <= 1 else sys.argv[1] 
	)
