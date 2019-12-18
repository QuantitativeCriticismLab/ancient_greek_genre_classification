#pylint: disable = C
import sys
import os
import numpy as np

from qcrit.analyze_models import _get_features, _get_file_classifications, _get_classifier_data
import qcrit.extract_features

from download_corpus import download_corpus

feature_data_file = sys.argv[1] if len(sys.argv) >= 2 else input('Enter pickle file to generate or extract: ')

if not os.path.isfile(feature_data_file):
	corpus_path = ('tesserae', 'texts', 'grc')
	download_corpus(corpus_path)

	from corpus_categories import composite_files
	from greek_features import * # pylint: disable = wildcard-import, unused-wildcard-import
	#Feature extractions
	qcrit.extract_features.main(
		os.path.join(*corpus_path),
		{'tess': qcrit.extract_features.parse_tess},
		#Exclude the following directories and files
		excluded_paths=composite_files,
		#Output the results to a file in order to be processed by machine learning algorithms
		output_file=feature_data_file
	)


classification_data_file = 'labels/prosody_labels.csv'

filename_to_features = _get_features(feature_data_file)

filename_to_classification, labels = _get_file_classifications(classification_data_file)

#For every set of features, there should be a corresponding file classification
assert len(filename_to_features.keys() - filename_to_classification.keys()) == 0, (
	'file_to_feature len: ' + str(len(filename_to_features.keys()))
	+ ', filename_to_classification len: ' + str(len(filename_to_classification.keys()))
)

#Convert features and classifications into sorted lists
file_names = sorted(filename_to_features.keys())
feature_names = sorted(
	list({feature for feature_to_val in filename_to_features.values() for feature in feature_to_val.keys()}))

data, target = _get_classifier_data(
	filename_to_features, filename_to_classification, file_names, feature_names
)

assert len(data) == len(target) == len(file_names)

code_repo = os.popen('git remote get-url origin').read().strip()
code_hash = os.popen('git rev-parse HEAD').read().strip()
corpus_repo = os.popen('git -C "./tesserae" remote get-url origin').read().strip()
corpus_hash = os.popen('git -C "./tesserae" rev-parse HEAD').read().strip()

prose_file = open(os.path.join('extracted_data', 'prose_data.csv'), mode='w')
prose_file.write('Ancient Greek Prose Data')
verse_file = open(os.path.join('extracted_data', 'verse_data.csv'), mode='w')
verse_file.write('Ancient Greek Verse Data')
for f in (prose_file, verse_file):
	first_line = (
		f',Code Repo: {code_repo}',
		f',Corpus: {corpus_repo}',
		f',Code commit: {code_hash}',
		f',Corpus commit: {corpus_hash}',
		f',Project: https://www.qcrit.org',
		f',Author: Tim Gianitsos',
		f',Note: Frequencies are per-character',
	)
	#having blank cells allows first row to match the dimensions of subsequent rows
	#this will cause it to display on Github better
	num_buffer_cells = data.shape[1] - len(first_line)

	f.write(''.join(first_line))
	f.write(',' * num_buffer_cells + '\n')
	f.write('file name,' + ','.join(feature_names) + '\n')

for i in range(len(data)):
	f = prose_file if filename_to_classification[file_names[i]] == np.float64(1) else verse_file
	f.write(file_names[i][file_names[i].rindex(os.sep) + 1:] + ',' + ','.join(str(e) for e in data[i]) + '\n')

print('Successfully generated csv files!')
