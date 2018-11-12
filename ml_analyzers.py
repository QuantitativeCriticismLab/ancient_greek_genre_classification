import sys
import numpy as np
import analyze_models
from functools import reduce
from sklearn import svm, neural_network, naive_bayes, ensemble, neighbors
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from color import RED, GREEN, YELLOW, PURPLE, RESET
from progress_bar import print_progress_bar
from collections import Counter
from model_analyzer import model_analyzer, decorated_analyzers

def _display_stats(expected, results, file_names, labels_key, tabs=0):
	assert len(expected) == len(results)

	#Obtain stats
	num_correct = reduce(lambda x, y: x + (1 if results[y] == expected[y] else 0), range(len(results)), 0)
	res_tuples = []
	for label_num in labels_key.keys():
		num_label_correct = reduce(lambda cur_tot, index: cur_tot + (1 if expected[index] == label_num 
			and results[index] == expected[index] else 0), range(len(results)), 0)
		num_label_total = reduce(lambda cur_tot, index: cur_tot + (1 if expected[index] == label_num 
			else 0), range(len(results)), 0)
		res_tuples.append((label_num, num_label_correct, num_label_total))

	#Display stats
	print('\t' * tabs + YELLOW + 'Stats:' + RESET)
	print('\t' * tabs + '# correct: ' + GREEN + str(num_correct) + RESET + ' / ' + str(len(expected)))
	print('\t' * tabs + '% correct: ' + GREEN + '%.4f' % (num_correct / len(results) * 100) + RESET + '%')
	for label_num, num_label_correct, num_label_total in res_tuples:
		print('\t' * tabs + '# %s: ' % labels_key[label_num] + GREEN + str(num_label_correct) + RESET 
			+ ' / ' + str(num_label_total))
		print('\t' * tabs + '%% %s: ' % labels_key[label_num] + GREEN + '%.4f' % 
			(num_label_correct / num_label_total * 100) + RESET + '%')
	print()

@model_analyzer()
def random_forest_test(data, target, file_names, feature_names, labels_key):
	print(RED + 'Random Forest tests' + RESET)

	features_train, features_test, labels_train, labels_test = train_test_split(data, target, test_size=0.4, random_state=0)
	clf = ensemble.RandomForestClassifier(random_state=0)
	clf.fit(features_train, labels_train)
	results = clf.predict(features_test)
	expected = labels_test
	tabs = 1

	print('\t' * tabs + YELLOW + 'RF parameters' + RESET + ' = ' + str(clf.get_params()) + '\n')
	_display_stats(expected, results, file_names, labels_key, tabs=tabs)
	print('\t' * tabs + YELLOW + 'Random Forest Gini Importance : Feature Name' + RESET)
	for t in sorted(zip(feature_names, clf.feature_importances_), key=lambda s: -s[1]):
		print('\t' * tabs + '%f: %s' % (t[1], t[0]))

@model_analyzer()
def random_forest_cross_validation(data, target, file_names, feature_names, labels_key):
	print(RED + 'Random Forest cross validation' + RESET)
	clf = ensemble.RandomForestClassifier(random_state=0)
	splitter = StratifiedKFold(n_splits=5, shuffle=False, random_state=0)
	tabs = 1

	print('\t' * tabs + YELLOW + 'RF parameters' + RESET + ' = ' + str(clf.get_params()))
	cur_fold = 1
	for train_indices, validate_indices in splitter.split(data, target):
		features_train, features_validate = data[train_indices], data[validate_indices]
		labels_train, labels_validate = target[train_indices], target[validate_indices]

		clf.fit(features_train, labels_train)
		results = clf.predict(features_validate)
		expected = labels_validate

		print()
		print('\t' * tabs + YELLOW + 'Validate fold ' + str(cur_fold) + ':' + RESET)
		_display_stats(expected, results, file_names, labels_key, tabs=tabs + 1)
		print('\t' * (tabs + 1) + YELLOW + 'Random Forest Gini Importance : Feature Name' + RESET)
		for t in sorted(zip(feature_names, clf.feature_importances_), key=lambda s: -s[1]):
			print('\t' * (tabs + 1) + '%f: %s' % (t[1], t[0]))

		cur_fold += 1

@model_analyzer()
def random_forest_misclassifications(data, target, file_names, feature_names, labels_key):
	misclass_counter = Counter()
	rf_trials = 20
	kfold_trials = 20
	splits = 5
	print(RED + 'Random Forest misclassifications' + RESET)
	print('Obtain misclassifications by testing different RF seeds and different data splits')
	print('RF seeds tested: 0-' + str(rf_trials - 1) + ' (inclusive)')
	print('Cross validation splitter seeds tested: 0-' + str(kfold_trials - 1) + ' (inclusive)')
	print('Number of splits: ' + str(splits))
	print('Features tested: ' + str(feature_names))
	print()

	trial_num = 1
	for rf_seed in range(rf_trials):
		clf = ensemble.RandomForestClassifier(random_state=rf_seed)
		for kfold_seed in range(kfold_trials):
			splitter = StratifiedKFold(n_splits=splits, shuffle=True, random_state=kfold_seed)
			current_fold = 0
			for train_indices, validate_indices in splitter.split(data, target):
				features_train, features_validate = data[train_indices], data[validate_indices]
				labels_train, labels_validate = target[train_indices], target[validate_indices]

				clf.fit(features_train, labels_train)
				results = clf.predict(features_validate)
				expected = labels_validate
				for i in range(len(results)):
					if results[i] != expected[i]:
						misclass_counter[file_names[validate_indices[i]]] += 1
				print_progress_bar(trial_num, rf_trials * kfold_trials * splits, prefix='Progress', 
					suffix='rf seed: %d, splitter seed: %d, fold: %d' % (rf_seed, kfold_seed, current_fold))
				trial_num += 1
				current_fold += 1

	print(YELLOW + 'Misclassifications from ' + str(rf_trials * kfold_trials * splits) + 
		' (' + str(rf_trials) + ' * ' + str(kfold_trials) + ' * ' + str(splits) + ') trials. ' + 
		'Each file was in the testing set 1 / ' + str(splits) + ' of the time (' + 
		str(rf_trials * kfold_trials) + ' times).' + RESET
	)
	largest_num_size = str(len(str(max(misclass_counter.values()))))
	for t in sorted([(val, cnt) for val, cnt in misclass_counter.items()], key=lambda s: -s[1]):
		print(('%' + largest_num_size + 'd / %d (%2.3f%%): %s') % 
			(t[1], rf_trials * kfold_trials, t[1] / rf_trials / kfold_trials * 100, t[0]))

@model_analyzer()
def random_forest_feature_rankings(data, target, file_names, feature_names, labels_key):
	rf_trials = 20
	kfold_trials = 20
	splits = 5
	feature_rankings = {name: np.zeros(rf_trials * kfold_trials * splits) for name in feature_names}
	print(RED + 'Random Forest feature rankings' + RESET)
	print('Obtain rankings by testing different RF seeds and different data splits')
	print('RF seeds tested: 0-' + str(rf_trials - 1) + ' (inclusive)')
	print('Cross validation splitter seeds tested: 0-' + str(kfold_trials - 1) + ' (inclusive)')
	print('Number of splits: ' + str(splits))
	print('Features tested: ' + str(feature_names))
	print()

	trial = 0
	for rf_seed in range(rf_trials):
		clf = ensemble.RandomForestClassifier(random_state=rf_seed)
		for kfold_seed in range(kfold_trials):
			splitter = StratifiedKFold(n_splits=splits, shuffle=True, random_state=kfold_seed)
			current_fold = 0
			for train_indices, validate_indices in splitter.split(data, target):
				features_train, features_validate = data[train_indices], data[validate_indices]
				labels_train, labels_validate = target[train_indices], target[validate_indices]

				clf.fit(features_train, labels_train)
				for t in zip(feature_names, clf.feature_importances_):
					feature_rankings[t[0]][trial] = t[1]
				trial += 1
				print_progress_bar(trial, rf_trials * kfold_trials * splits, prefix='Progress', 
					suffix='rf seed: %d, splitter seed: %d, fold: %d' % (rf_seed, kfold_seed, current_fold))
				current_fold += 1

	print(YELLOW + 'Gini averages from ' + str(rf_trials * kfold_trials * splits) + 
		' (' + str(rf_trials) + ' * ' + str(kfold_trials) + ' * ' + str(splits) + ') trials' + RESET)
	for t in sorted([(feat, rank) for feat, rank in feature_rankings.items()], key=lambda s: -1 * s[1].mean()):
		print('\t' + '%.6f +/- standard deviation of %.4f' % (t[1].mean(), t[1].std()) + ': ' + t[0])

@model_analyzer()
def sample_classifiers(data, target, file_names, feature_names, labels_key):
	#Includes all the machine learning classifiers
	classifiers = [
		ensemble.RandomForestClassifier(random_state=0), 
		svm.SVC(gamma=0.00001, kernel='rbf', random_state=0), 
		naive_bayes.GaussianNB(priors=None), 
		neighbors.KNeighborsClassifier(n_neighbors=5), 
		neural_network.MLPClassifier(activation='relu', solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(12,), random_state=0), 
	]
	features_train, features_test, labels_train, labels_test = train_test_split(data, target, test_size=0.4, random_state=5)

	print(RED + 'Miscellaneous machine learning models:' + RESET)

	tabs = 1
	for clf in classifiers:
		print('\n' + PURPLE + '\t' * tabs + clf.__class__.__name__ + RESET)

		#Parameters used in creating this classifier
		print('\t' * (tabs + 1) + 'Parameters: ' + str(clf.get_params()))
		print()

		#Train & predict classifier
		clf.fit(features_train, labels_train)
		results = clf.predict(features_test)
		expected = labels_test

		_display_stats(expected, results, file_names, labels_key, tabs + 1)

		#Cross validation
		scores = cross_val_score(clf, features_train, labels_train, cv=5)
		print('\t' * (tabs + 1) + YELLOW + 'Cross Validation:' + RESET)
		print('\t' * (tabs + 1) + 'Scores: ' + str(scores))
		print('\t' * (tabs + 1) + 'Avg Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std() * 2))

if __name__ == '__main__':
	analyze_models.main(
		sys.argv[1] if len(sys.argv) > 1 else input('Enter filename to extract feature data: '), 
		sys.argv[2] if len(sys.argv) > 2 else input('Enter filename to extract classification data: '), 
		sys.argv[3] if len(sys.argv) > 3 else input('What would you like to do?\n' + 
		'\n'.join(('\t' + name for name in decorated_analyzers)) + '\n'
		)
	)
