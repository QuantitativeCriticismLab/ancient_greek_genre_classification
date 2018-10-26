import os
import numpy as np
import pickle
from analyze_models import _get_features, _get_file_classifications, _get_classifier_data

feature_data_file = 'notes/feature_data.pickle'

if not os.path.isfile(feature_data_file):
	#Download corpus if non-existent
	corpus_dir = os.path.join('tesserae', 'texts', 'grc')
	tesserae_clone_command = 'git clone https://github.com/timgianitsos/tesserae.git'
	if not os.path.isdir(corpus_dir):
		print(RED + 'Corpus at ' + corpus_dir + ' does not exist - attempting to clone repository...' + RESET)
		if os.system(tesserae_clone_command) is not 0:
			raise Exception('Unable to obtain corpus for feature extraction')


	from greek_features import composite_files_to_exclude
	import extract_features
	#Feature extractions
	extract_features.main(
		corpus_dir, 
		'tess', 

		#Exclude the following directories and files
		excluded_paths=composite_files_to_exclude,

		#Only extract the following features
		# features=['freq_men'], 

		#Output the results to a file in order to be processed by machine learning algorithms
		output_file=feature_data_file
	)


classification_data_file = 'classifications.csv'

filename_to_features = _get_features(feature_data_file)

filename_to_classification = _get_file_classifications(classification_data_file)

#For every set of features, there should be a corresponding file classification
assert len(filename_to_features.keys() - filename_to_classification.keys()) == 0, 'file_to_feature len: ' + str(len(filename_to_features.keys())) + ', filename_to_classification len: ' + str(len(filename_to_classification.keys()))

#Convert features and classifications into sorted lists
file_names = sorted([elem for elem in filename_to_features.keys()])
feature_names = sorted(list({feature for feature_to_val in filename_to_features.values() for feature in feature_to_val.keys()}))

data, target = _get_classifier_data(filename_to_features, filename_to_classification, file_names, feature_names)

assert len(data) == len(target) == len(file_names)

code_hash = os.popen('git rev-parse HEAD').read().strip()
tesserae_hash = os.popen('git -C "./tesserae" rev-parse HEAD').read().strip()
prose_file = open('prose_data.csv', mode='w')
prose_file.write('Ancient Greek Prose Data\n')
verse_file = open('verse_data.csv', mode='w')
verse_file.write('Ancient Greek Verse Data\n')
for f in (prose_file, verse_file):
	f.write('Data: https://github.com/timgianitsos/tesserae/tree/master/texts/grc,Project: https://www.qcrit.org,Author: Tim Gianitsos (tgianitsos@yahoo.com),Repo (Private): https://github.com/jdexter476/ProseVerseClassification.git,Code commit: ' + code_hash + ',Corpus commit: ' + tesserae_hash + ',Note: Frequencies are per-character\n')
	f.write('file name,' + ','.join(feature_names) + '\n')

for i in range(len(data)):
	f = prose_file if filename_to_classification[file_names[i]] == np.float64(1) else verse_file
	f.write(file_names[i][file_names[i].rindex(os.sep) + 1:] + ',' + ','.join(str(e) for e in data[i]) + '\n')

print('Success!')
