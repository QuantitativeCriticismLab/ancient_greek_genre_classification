# -*- coding: utf-8 -*-
#This file may not work on windows because it uses unix based commands

#************************************************************************************************************************
'''
0) Setup (only necessary for demo if first run through)
'''

import os
if not os.path.isdir('demo_files'):
	os.system('mkdir demo_files')
	repo = 'https://github.com/timgianitsos/tesserae.git'
	if not os.path.isdir('tesserae'):
		res = os.system('git clone ' + repo)
		if res is not 0:
			raise Exception('Unable to obtain corpus for feature extraction')

	grc_dir = os.path.join('tesserae', 'texts', 'grc')
	os.system('cp ' + os.path.join(grc_dir, 'aristophanes.ecclesiazusae.tess') + ' demo_files')
	os.system('cp ' + os.path.join(grc_dir, 'aristotle.metaphysics.tess') + ' demo_files')
	os.system('cp ' + os.path.join(grc_dir, 'euripides.heracles.tess') + ' demo_files')
	os.system('cp ' + os.path.join(grc_dir, 'plato.respublica.tess') + ' demo_files')
	f = open(os.path.join('demo_files', 'classifications.csv'), mode='w')
	f.write('verse:0,prose:1\n')
	f.write('Filename,Label\n')
	f.write(os.path.join('demo_files', 'aristophanes.ecclesiazusae.tess') + ',0\n')
	f.write(os.path.join('demo_files', 'aristotle.metaphysics.tess') + ',1\n')
	f.write(os.path.join('demo_files', 'euripides.heracles.tess') + ',0\n')
	f.write(os.path.join('demo_files', 'plato.respublica.tess') + ',1\n')
	f.close()

#If the output file already exists, the feature extraction code will not override it
#Delete the output file so that the demo can create one
if os.path.isfile(os.path.join('demo_files', 'output.pickle')):
	os.system('rm ' + os.path.join('demo_files', 'output.pickle'))

#************************************************************************************************************************
'''
1) Extract the features

A feature is some quantitative measure extracted by analyzing the text in a file. 
Examples of features include the mean sentence length of a file or the frequency of conjunctions in a file.

Use the python decorator textual_feature to create a feature.

@textual_feature()
def foo(file): #must have one parameter which is assumed be the parsed text of a file
	return 0

The textual_feature decorator takes two optional arguments: the type of tokenization, and the language.

@textual_feature(tokenize_type='sentences', lang='ancient_greek')
def bar(file):
	return 0

There are four supported tokenization_types: 'sentences', 'words', 'sentence_words' and None. This tells the function in 
what format it will receive the 'file' parameter.
- If None, the function will receive the file parameter as a string. 
- If 'sentences', the function will receive the file parameter as a list of sentences, each as a string
- If 'words', the function will receive the file parameter as a list of words
- If 'sentence_words', the function will recieve the file parameter as a list of sentences, each as a list of words

There are several supported lang options: None, 'greek', 'estonian', 'ancient_greek', 'turkish', 'polish', 
'czech', 'portuguese', 'dutch', 'norwegian', 'slovene', 'english', 'danish', 'finnish', 'swedish', 
'spanish', 'german', 'italian', 'french'

If the language needed is not in this list, using None will often suffice. The lang option is used only 
in sentence tokenization. It's purpose is to help the sentence tokenizer identify abbreviations in a 
given language (so that it doesn't mistake an abbreviation as a sentence ending). If there are very few 
abbreviation in a corpus, the utility of specifying the language will be marginal.

Use extract_features.main to run all the functions labeled with the decorators, and output results into a file

extract_features.main(corpus_dir='demo_files', file_extension='tess', output_file=os.path.join('demo_files', 'output.pickle'))

corpus_dir - the directory to search for files containing texts, this will traverse all sub-directories as well
file_extension - restrict search to only files with this extension, handles parsing out of unnecessary tags, 
                 currently only supports .tess but easily extensible to xml, txt, etc.
output_file - the file to output the results into, created to be analyzed during machine learning phase

In order for sentence tokenization to work correctly, setup_tokenizers() must be set to the 
terminal punctuation marks of the language being analyzed. Make sure this is done before main() is called.
'''
import extract_features
from textual_feature import textual_feature, setup_tokenizers
from functools import reduce
from unicodedata import normalize

#Let sentence tokenizer know that periods and semicolons are the punctuation marks that end sentences
setup_tokenizers(terminal_punctuation=('.', ';'), language='ancient_greek')

@textual_feature(tokenize_type='words') #Using 'words' makes the input 'file' parameter become a list of words
def num_conjunctions(file): #parameter must be the text of a file
	return reduce(lambda count, word: count + (1 if word in {normalize('NFD', val) for val in ['καί', 'καὶ', 'ἀλλά', 'ἀλλὰ', 'ἤ', 'ἢ']} else 0), file, 0)

@textual_feature(tokenize_type='sentences') #Using 'sentences' makes the input 'file' parameter become a list of sentences
def mean_sentence_length(file): #parameter must be the text of a file
	return reduce(lambda count, sentence: count + len(sentence), file, 0) / len(file)

@textual_feature() #Not putting any decorator parameters will leave the input 'file' parameter unchanged as a string of text
def num_interrogatives(file): #parameter must be the text of a file
	return file.count(';')


extract_features.main(corpus_dir='demo_files', file_extension='tess', output_file=os.path.join('demo_files', 'output.pickle'))
'''
Extracting features from .tess files in demo_files
Progress |███████████████████████████████████████████| 100.0% (4 of 4 files)
Feature mining complete. Attempting to write feature results to "demo_files/output.pickle"...
Success!


Elapsed time: 1.262120753992349
'''

#************************************************************************************************************************
'''
2) Train & Test machine learning models on the features

Use the "@model_analyzer()" decorator to label functions that analyze machine learning models

Invoke "analyze_models.main('demo_files/output.pickle', 'demo_files/classifications.csv')" to 
run all functions labeled with the "@model_analyzer()" decorator. To run only one function, include 
the name of the function as the third parameter to analyze_models.main()

output.pickle: Now that the features have been extracted and output into output.pickle, we 
can use machine learning models on them.

classifications.csv: The file classifications.csv contains the name of the file in the first column 
and the particular classification (prose or verse) in the second column for every file in the corpus.
'''
import analyze_models
from model_analyzer import model_analyzer
from sklearn import ensemble, neural_network, svm
from sklearn.model_selection import train_test_split

@model_analyzer()
def random_forest_analyzer(data, target, file_names, feature_names, labels_key):
	print('-' * 40 + '\nRandom Forest Classifier\n')
	features_train, features_test, labels_train, labels_test = train_test_split(data, target, test_size=0.5, random_state=0)
	clf = ensemble.RandomForestClassifier(random_state=0)
	clf.fit(features_train, labels_train)
	results = clf.predict(features_test)

	#Display features in order of importance
	print('Feature importances:')
	for t in sorted(zip(feature_names, clf.feature_importances_), key=lambda s: -s[1]):
		print('\t%f: %s' % (t[1], t[0]))

@model_analyzer()
def neural_net_analyzer(data, target, file_names, feature_names, labels_key):
	print('-' * 40 + '\nMultilayer Perceptron\n')
	features_train, features_test, labels_train, labels_test = train_test_split(data, target, test_size=0.5, random_state=0)
	clf = neural_network.MLPClassifier(activation='relu', solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(12,), random_state=0)
	clf.fit(features_train, labels_train)
	results = clf.predict(features_test)

	num_correct = reduce(lambda x, y: x + (1 if results[y] == target[y] else 0), range(len(results)), 0)
	print('Stats:')
	print('\tNumber correct: ' + str(num_correct) + ' / ' + str(len(target)))
	print('\tPercentage correct: ' + str(num_correct / len(target)) + '%')

@model_analyzer()
def support_vector_machine_analyzer(data, target, file_names, feature_names, labels_key):
	print('-' * 40 + '\nSupport Vector Machine\n')
	features_train, features_test, labels_train, labels_test = train_test_split(data, target, test_size=0.5, random_state=1)
	clf = svm.SVC(gamma=0.00001, kernel='rbf', random_state=0)
	clf.fit(features_train, labels_train)
	results = clf.predict(features_test)

	print('Misclassifications:')
	found_misclassification = False
	for j in range(len(results)):
		if results[j] != target[j]:
			print('\t' + file_names[j])
			found_misclassification = True
	print('No misclassifications!' if not found_misclassification else '', end='')

analyze_models.main('demo_files/output.pickle', 'demo_files/classifications.csv')
'''
----------------------------------------
Random Forest Classifier

Feature importances:
	0.200000: num_conjunctions
	0.200000: num_interrogatives
	0.100000: mean_sentence_length


Elapsed time: 0.011877743992954493

----------------------------------------
Multilayer Perceptron

Stats:
	Number correct: 1 / 4
	Percentage correct: 0.25%


Elapsed time: 0.005417105043306947

----------------------------------------
Support Vector Machine

Misclassifications:
	demo_files/aristophanes.ecclesiazusae.tess
	demo_files/aristotle.metaphysics.tess


Elapsed time: 0.0010444470099173486

'''
