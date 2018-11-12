import os
import pickle
import numpy as np
from model_analyzer import decorated_analyzers
from color import GREEN, RESET
from functools import partial
from collections import OrderedDict

def _get_features(feature_data_file):
	#Obtain features that were previously mined and serialized into a file
	filename_to_features = None
	with open(feature_data_file, mode='rb') as pickle_file:
		filename_to_features = pickle.loads(pickle_file.read())
	return filename_to_features

#TODO handle backslash-commas in the csv (they are meant to be read literally and do NOT demarcate a csv cell)
def _get_file_classifications(classification_data_file):
	#Obtain classifications for each file
	filename_to_classification = {}
	with open(classification_data_file, mode='r') as classification_file:
		labels_key = OrderedDict(
			(np.float64(tok.split(':')[1]), tok.split(':')[0]) for tok in classification_file.readline().strip().split(',')
		)
		classification_file.readline()
		for line in classification_file:
			line = line.strip().split(',')
			filename_to_classification[line[0]] = np.float64(line[1])
		assert all(v in labels_key.keys() for v in filename_to_classification.values())
	return filename_to_classification, labels_key

def _get_classifier_data(filename_to_features, filename_to_classification, file_names, feature_names):
	data_1d = [filename_to_features[file_name][feature] for file_name in file_names for feature in feature_names]
	data = []
	for i in range(len(file_names)):
		data.append([val for val in data_1d[i * len(feature_names): i * len(feature_names) + len(feature_names)]])
	target = [filename_to_classification[file_name] for file_name in file_names]

	assert data[-1][-1] == data_1d[-1]
	assert len(data) == len(target)
	assert len(data) == len(file_names)
	assert len(feature_names) == len(data[0])

	#Convert lists to numpy arrays so they can be used in the machine learning models
	data = np.asarray(data)
	target = np.asarray(target)
	return (data, target)

def main(feature_data_file, classification_data_file, model_func=None):
	assert os.path.isfile(feature_data_file), 'File "' + feature_data_file + '" does not exist'
	assert os.path.isfile(classification_data_file), 'File "' + classification_data_file + '" does not exist'
	assert model_func is None or model_func in decorated_analyzers, '"' + model_func + '" is not a decorated model analyzer'

	filename_to_features = _get_features(feature_data_file)

	filename_to_classification, labels_key = _get_file_classifications(classification_data_file)

	assert len(filename_to_features.keys() - filename_to_classification.keys()) == 0

	#Convert features and classifications into sorted lists
	file_names = sorted([elem for elem in filename_to_features.keys()])
	feature_names = sorted(list({feature for feature_to_val in filename_to_features.values() for feature in feature_to_val.keys()}))

	data, target = _get_classifier_data(filename_to_features, filename_to_classification, file_names, feature_names)

	from timeit import timeit
	if model_func:
		print('\n\n' + GREEN + 'Elapsed time: ' + 
			str(timeit(partial(decorated_analyzers[model_func], data, target, file_names, feature_names, labels_key), number=1)) + 
			' seconds' + RESET
		)
	else:
		for func in decorated_analyzers.values():
			print('\n\n' + GREEN + 'Elapsed time: ' + 
				str(timeit(partial(func, data, target, file_names, feature_names, labels_key), number=1)) + ' seconds' + RESET + '\n'
			)
