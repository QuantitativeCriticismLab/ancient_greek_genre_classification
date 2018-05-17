import pickle
import math
import numpy as np
from functools import reduce
from sklearn import svm, neural_network, naive_bayes, ensemble, neighbors
from sklearn.model_selection import train_test_split, cross_val_score

GREEN = '\033[92m'
YELLOW = '\033[93m'
PURPLE = '\033[95m'
RESET = '\033[0m'

def main():

	#Obtain classifications (prose or verse) for each file
	file_to_isprose = {}
	with open('classifications.csv', mode='r') as classification_file:
		classification_file.readline()
		for line in classification_file:
			line = line.strip().split(',')
			file_to_isprose[line[0]] = 1 if line[1] == 'True' else 0

	#Obtain features that were previously mined and serialized into a file
	text_to_features = None
	with open('matrix.pickle', mode='rb') as pickle_file:
		text_to_features = pickle.loads(pickle_file.read())
	
	#Convert features and classifications into sorted lists
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

	#Convert lists to numpy arrays so they can be used in the machine learning models
	data = np.asarray(data)
	target = np.asarray(target)

	features_train, features_test, labels_train, labels_test = train_test_split(data, target, test_size=0.4, random_state=1)

	#Includes all the machine learning classifiers
	classifiers = [\
	ensemble.RandomForestClassifier(random_state=1), \
	svm.SVC(gamma=0.00001, kernel='rbf', random_state=0), \
	naive_bayes.GaussianNB(priors=None), \
	neighbors.KNeighborsClassifier(n_neighbors=5), \
	neural_network.MLPClassifier(activation='relu', solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(12,), random_state=0)]

	print('Test files: ' + str(len(labels_test)))
	for clf in classifiers:
		print(PURPLE + clf.__class__.__name__ + RESET)

		#Cross validation
		scores = cross_val_score(clf, features_train, labels_train, cv=5)
		print('\t' + YELLOW + 'Cross Validation:' + RESET)
		print('\tScores: ' + str(scores))
		print('\tAvg Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std() * 2))

		#Train & predict classifier
		clf.fit(features_train, labels_train)
		results = clf.predict(features_test)
		expected = labels_test

		#Obtain stats
		num_correct = reduce(lambda x, y: x + (1 if results[y] == expected[y] else 0), range(len(results)), 0)
		num_prose_correct = reduce(lambda x, y: x + (1 if results[y] == expected[y] and expected[y] == 1 else 0), \
		range(len(results)), 0)
		num_prose = reduce(lambda x, y: x + (1 if expected[y] == 1 else 0), range(len(results)), 0)
		num_verse_correct = reduce(lambda x, y: x + (1 if results[y] == expected[y] and expected[y] == 0 else 0), \
		range(len(results)), 0)
		num_verse = reduce(lambda x, y: x + (1 if expected[y] == 0 else 0), range(len(results)), 0)

		#Display stats
		print('\t' + YELLOW + 'Testing:' + RESET)
		print('\t# correct: ' + GREEN + str(num_correct) + RESET + ' / ' + str(len(labels_test)))
		print('\t% correct: ' + GREEN + '%.4f' % (num_correct / len(results) * 100) + RESET + '%')
		print('\t# prose: ' + GREEN + str(num_prose_correct) + RESET + ' / ' + str(num_prose))
		print('\t% prose: ' + GREEN + '%.4f' % (num_prose_correct / num_prose * 100) + RESET + '%')
		print('\t# verse: ' + GREEN + str(num_verse_correct) + RESET + ' / ' + str(num_verse))
		print('\t% verse: ' + GREEN + '%.4f' % (num_verse_correct / num_verse * 100) + RESET + '%')

	print('Random Forest Gini Importance: Feature Name')
	for t in sorted(zip(feature_names, classifiers[0].feature_importances_), key=lambda s: -s[1]):
		print('%f: %s' % (t[1], t[0]))
	print(classifiers[0].get_params())

if __name__ == '__main__':
	main()
