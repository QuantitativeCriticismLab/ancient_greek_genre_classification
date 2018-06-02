import pickle
import math
import numpy as np
from functools import reduce
from sklearn import svm, neural_network, naive_bayes, ensemble, neighbors
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from color import RED, GREEN, YELLOW, PURPLE, RESET
from collections import Counter

def get_file_classifications():
	#Obtain classifications (prose or verse) for each file
	file_to_isprose = {}
	with open('classifications.csv', mode='r') as classification_file:
		classification_file.readline()
		for line in classification_file:
			line = line.strip().split(',')
			file_to_isprose[line[0]] = 1 if line[1] == 'True' else 0
	return file_to_isprose

def get_features():
	#Obtain features that were previously mined and serialized into a file
	text_to_features = None
	with open('matrix.pickle', mode='rb') as pickle_file:
		text_to_features = pickle.loads(pickle_file.read())
	return text_to_features

def get_classifier_data(file_to_isprose, text_to_features, file_names, feature_names):
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
	return (data, target)

def display_stats(expected, results, tabs=0):
	assert len(expected) == len(results)

	#Obtain stats
	num_correct = reduce(lambda x, y: x + (1 if results[y] == expected[y] else 0), range(len(results)), 0)
	num_prose_correct = reduce(lambda x, y: x + (1 if results[y] == expected[y] and expected[y] == 1 else 0), \
	range(len(results)), 0)
	num_prose = reduce(lambda x, y: x + (1 if expected[y] == 1 else 0), range(len(results)), 0)
	num_verse_correct = reduce(lambda x, y: x + (1 if results[y] == expected[y] and expected[y] == 0 else 0), \
	range(len(results)), 0)
	num_verse = reduce(lambda x, y: x + (1 if expected[y] == 0 else 0), range(len(results)), 0)

	#Display stats
	print('\t' * tabs + YELLOW + 'Testing:' + RESET)
	print('\t' * tabs + '# correct: ' + GREEN + str(num_correct) + RESET + ' / ' + str(len(expected)))
	print('\t' * tabs + '% correct: ' + GREEN + '%.4f' % (num_correct / len(results) * 100) + RESET + '%')
	print('\t' * tabs + '# prose: ' + GREEN + str(num_prose_correct) + RESET + ' / ' + str(num_prose))
	print('\t' * tabs + '% prose: ' + GREEN + '%.4f' % (num_prose_correct / num_prose * 100) + RESET + '%')
	print('\t' * tabs + '# verse: ' + GREEN + str(num_verse_correct) + RESET + ' / ' + str(num_verse))
	print('\t' * tabs + '% verse: ' + GREEN + '%.4f' % (num_verse_correct / num_verse * 100) + RESET + '%')

def random_forest_test(features_train, features_test, labels_train, labels_test, file_names, feature_names):
	print(RED + 'Random Forest tests\n' + RESET)

	trials = 10
	for seed in range(trials):
		print(PURPLE + 'Seed ' + str(seed) + RESET)
		clf = ensemble.RandomForestClassifier(random_state=seed)
		clf.fit(features_train, labels_train)
		results = clf.predict(features_test)
		expected = labels_test
		print('\t' + YELLOW + 'Misclassifications:' + RESET)
		found_misclassification = False
		for j in range(len(results)):
			if results[j] != expected[j]:
				print('\t' + file_names[j])
				found_misclassification = True
		print(('\t' + GREEN + 'No misclassifications!\n' + RESET) if not found_misclassification else '')
		print('\t' + YELLOW + 'Random Forest Gini Importance : Feature Name' + RESET)
		for t in sorted(zip(feature_names, clf.feature_importances_), key=lambda s: -s[1]):
			print('\t%f: %s' % (t[1], t[0]))
		print()

def random_forest_cross_validation(data, target, file_names):
	print(RED + 'Random Forest cross validation\n' + RESET)

	trials = 10
	splitter = StratifiedKFold(n_splits=5, shuffle=False, random_state=0)
	for seed in range(trials):
		print(PURPLE + 'Seed ' + str(seed) + RESET)
		cur_fold = 1
		clf = ensemble.RandomForestClassifier(random_state=seed)
		print('\tRF parameters = ' + str(clf.get_params()))

		for train_indices, validate_indices in splitter.split(data, target):
			features_train, features_validate = data[train_indices], data[validate_indices]
			labels_train, labels_validate = target[train_indices], target[validate_indices]

			clf.fit(features_train, labels_train)
			results = clf.predict(features_validate)
			expected = labels_validate

			print('\t' + YELLOW + 'Validate fold ' + str(cur_fold) + ':' + RESET)
			print('\t\t' + YELLOW + 'Misclassifications: ' + RESET)
			found_misclassification = False
			for i in range(len(results)):
				if results[i] != expected[i]:
					print('\t\t' + file_names[i])
					found_misclassification = True
			print(end=('\t\t' + GREEN + 'No misclassifications!' + RESET + '\n') if not found_misclassification else '')

			display_stats(expected, results, 2)
			print()

			cur_fold += 1

def random_forest_misclassifications(data, target, file_names, feature_names):
	misclass_counter = Counter()
	rf_trials = 15
	kfold_trials = 15
	splits = 5
	print(RED + 'Random Forest misclassifications' + RESET)
	print('Obtain misclassifications by testing different RF seeds and different data splits')
	print('RF seeds tested: (0-' + str(rf_trials - 1) + ')')
	print('Cross validation splitter seeds tested: (0-' + str(kfold_trials - 1) + ')')
	print('Features tested: (1-' + str(len(feature_names)) + ')')
	print('Number of splits: ' + str(splits))
	print()

	for rf_seed in range(rf_trials):
		clf = ensemble.RandomForestClassifier(random_state=rf_seed)
		for kfold_seed in range(kfold_trials):
			splitter = StratifiedKFold(n_splits=splits, shuffle=True, random_state=kfold_seed)
			for train_indices, validate_indices in splitter.split(data, target):
				features_train, features_validate = data[train_indices], data[validate_indices]
				labels_train, labels_validate = target[train_indices], target[validate_indices]

				clf.fit(features_train, labels_train)
				results = clf.predict(features_validate)
				expected = labels_validate
				for i in range(len(results)):
					if results[i] != expected[i]:
						misclass_counter[file_names[i]] += 1
	for t in sorted([(val, cnt) for val, cnt in misclass_counter.items()], key=lambda s: -s[1]):
		print(t[0] + ': ' + str(t[1]))

def sample_classifiers(features_train, features_test, labels_train, labels_test):
	#Includes all the machine learning classifiers
	classifiers = [\
	ensemble.RandomForestClassifier(random_state=0), \
	svm.SVC(gamma=0.00001, kernel='rbf', random_state=0), \
	naive_bayes.GaussianNB(priors=None), \
	neighbors.KNeighborsClassifier(n_neighbors=5), \
	neural_network.MLPClassifier(activation='relu', solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(12,), random_state=0)]

	print(RED + 'Miscellaneous machine learning models:\n' + RESET)

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

		display_stats(expected, results, 1)

		print('\t' + str(clf.get_params()))
		print()

def main():

	file_to_isprose = get_file_classifications()

	text_to_features = get_features()
	
	#Convert features and classifications into sorted lists
	file_names = sorted([elem for elem in text_to_features.keys()])
	feature_names = sorted(list({feature for feature_to_val in text_to_features.values() for feature in feature_to_val.keys()} \

		#Uncomment to exclude features 6-10 (ranked by average gini score)
		# - {'mean_sentence_length', 'freq_ws', 'freq_men', 'particles_per_sentence', 'freq_wste_not_preceded_by_eta'} \

		#Uncomment to exclude features 11-24 (ranked by average gini score)
		# - {'freq_temporal_and_causal_clauses', 'freq_superlative', 'freq_interrogatives', 'mean_length_relative_clause', \
		# 'freq_conditional_characters', 'freq_vocative_sentences', 'relative_clause_per_sentence', 'freq_personal_pronouns', \
		# 'freq_allos', 'non_interoggative_sentence_with_relative_clause', 'freq_purpose_clause', \
		# 'freq_indefinite_pronoun_in_non_interrogative_sentence', 'freq_indefinite_pronoun_in_any_sentence', \
		# 'freq_circumstantial_participial_clauses'}\
		))


	data, target = get_classifier_data(file_to_isprose, text_to_features, file_names, feature_names)

	features_train, features_test, labels_train, labels_test = train_test_split(data, target, test_size=0.4, random_state=5)

	# random_forest_test(features_train, features_test, labels_train, labels_test, file_names, feature_names)
	# random_forest_cross_validation(data, target, file_names)
	random_forest_misclassifications(data, target, file_names, feature_names)
	# sample_classifiers(features_train, features_test, labels_train, labels_test)

	# Test whether different seeds give different results for StratifiedKFold
	# seeds = 20
	# splits = 5
	# for i in range(seeds):
	# 	splitter1 = StratifiedKFold(n_splits=splits, shuffle=True, random_state=i)
	# 	for j in range(i + 1, seeds):
	# 		splitter2 = StratifiedKFold(n_splits=splits, shuffle=True, random_state=j)
	# 		t1 = list(splitter1.split(data, target))
	# 		t2 = list(splitter2.split(data, target))
	# 		for k in range(splits):
	# 			print('Identical? ' + str(not (False in (t1[k][0] == t2[k][0]))))

	# Find ratios of verse to total with different cross validators
	# print('Total verse percentage: ' + str(reduce(lambda x, y: x + (1 if y == 0 else 0), target, 0) / len(target)) + '\n')
	# from sklearn.model_selection import KFold, ShuffleSplit
	# splitters = [\
	# 	KFold(n_splits=5, shuffle=True, random_state=0), \
	# 	StratifiedKFold(n_splits=5, shuffle=True, random_state=0)\
	# 	]
	# tups = [list(splitter.split(data, target)) for splitter in splitters]
	# for splitter_index in range(len(splitters)):
	# 	tup = tups[splitter_index]
	# 	for i in range(len(tup)):
	# 		labels_train = target[tup[i][0]]
	# 		print(splitters[splitter_index].__class__.__name__ + ' ' + str(i) + ' verse percentage: ' + \
	# 			str(reduce(lambda x, y: x + (1 if y == 0 else 0), labels_train, 0) / len(labels_train)))

if __name__ == '__main__':
	main()
