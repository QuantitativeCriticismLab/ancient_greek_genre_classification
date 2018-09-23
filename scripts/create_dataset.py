import numpy as np
import pickle
from analyze_models import _get_features, _get_file_classifications, _get_classifier_data

feature_data_file = 'ut_dataset.pickle'
classification_data_file = 'classifications.csv'

filename_to_features = _get_features(feature_data_file)

filename_to_classification = _get_file_classifications(classification_data_file)

assert len(filename_to_features.keys() - filename_to_classification.keys()) == 0

#Convert features and classifications into sorted lists
file_names = sorted([elem for elem in filename_to_features.keys()])
feature_names = sorted(list({feature for feature_to_val in filename_to_features.values() for feature in feature_to_val.keys()}))

data, target = _get_classifier_data(filename_to_features, filename_to_classification, file_names, feature_names)

assert len(data) == len(target) == len(file_names)

#TODO Put labels, put, commit message, ensure data integrity
prose_file = open('prose_data.csv', mode='w')
prose_file.write('Ancient Greek Prose Data\n')
verse_file = open('verse_data.csv', mode='w')
verse_file.write('Ancient Greek Verse Data\n')
for f in (prose_file, verse_file):
	f.write('Data: https://github.com/timgianitsos/tesserae/tree/master/texts/grc,Project: https://www.qcrit.org,Author: Tim Gianitsos (tgianitsos@yahoo.com),Repo (Private): https://github.com/jdexter476/ProseVerseClassification.git,Commit: 79b6ffd129e13539ffa1c0eb6928e24852eb8ef1,Note: Frequencies are per-character\n')
	f.write('File name,' + ','.join(feature_names) + '\n')

for i in range(len(data)):
	f = prose_file if filename_to_classification[file_names[i]] == np.float64(1) else verse_file
	f.write(file_names[i][file_names[i].rindex('/') + 1:] + ',' + ','.join(str(e) for e in data[i]) + '\n')

print('Success!')