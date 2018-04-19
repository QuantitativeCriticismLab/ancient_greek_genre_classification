import pickle
import math
import numpy as np
from functools import reduce
from sklearn import svm, neural_network, naive_bayes

def main():
	file_to_isprose = {}
	with open('classifications.csv', mode='r') as classification_file:
		classification_file.readline()
		for line in classification_file:
			line = line.strip().split(',')
			file_to_isprose[line[0]] = 1 if line[1] == 'True' else 0

	text_to_features = None
	with open('matrix.pickle', mode='rb') as pickle_file:
		text_to_features = pickle.loads(pickle_file.read())
	
	file_names = sorted([elem for elem in text_to_features.keys()])
	feature_names = sorted(list({feature for feature_to_val in text_to_features.values() for feature in feature_to_val.keys()} \
	- {'freq_vocative_sentences', 'ratio_ina_to_opos', 'freq_wste_precceded_by_eta', 'freq_raised_dot'}))
	data_1d = [text_to_features[file_name][feature] for file_name in file_names for feature in feature_names]
	data = []
	for i in range(len(file_names)):
		data.append([val if str(val) != 'nan' and val != math.inf else 1000 \
		for val in data_1d[i * len(feature_names): i * len(feature_names) + len(feature_names)]])
	target = [file_to_isprose[file_name] for file_name in file_names]

	assert data[-1][-1] == data_1d[-1]
	assert len(data) == len(target)
	assert len(feature_names) == len(data[0])

	data = np.asarray(data)
	target = np.asarray(target)

	test_size = 289
	classifiers = [svm.SVC(gamma=0.00001, kernel='rbf'), neural_network.MLPClassifier(activation='relu', solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(12,)), naive_bayes.GaussianNB()]
	for clf in classifiers:
		clf.fit(data[:-test_size], target[:-test_size])
		results = clf.predict(data[-test_size:])
		expected = target[-test_size:]
		print("%-20s" % clf.__class__.__name__ + \
		("%.4f" % (reduce(lambda x, y: x + (1 if results[y] == expected[y] else 0), range(len(results)), 0) \
		/ len(results) * 100)) + "%")


if __name__ == '__main__':
	main()
