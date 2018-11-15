# -*- coding: utf-8 -*-

import extract_features
import sys
import os
from os.path import join
from textual_feature import textual_feature, setup_tokenizers
from color import RED, RESET
from functools import reduce
from nltk.tokenize.punkt import PunktLanguageVars
from unicodedata import normalize
#Reference: https://jktauber.com/articles/python-unicode-ancient-greek/

setup_tokenizers(('.', ';', ';')) #'FULL STOP', 'SEMICOLON', 'GREEK QUESTION MARK'

@textual_feature('sentence_words', 'ancient_greek')
def freq_interrogatives(file):
	num_interrogative = 0
	interrogative_chars = {';', ';'}
	for line in file:
		num_interrogative += reduce(lambda cur_count, word: cur_count + 1 if word in interrogative_chars else 0, line, 0)

	return num_interrogative / len(file)

@textual_feature('words', 'ancient_greek')
def freq_conditional_words(file):
	num_conditional_words = 0
	num_characters = 0
	conditional_words = {'εἰ', 'εἴ', 'εἲ', 'ἐάν', 'ἐὰν'}
	conditional_words = conditional_words | \
	{normalize('NFD', val) for val in conditional_words} | \
	{normalize('NFC', val) for val in conditional_words} | \
	{normalize('NFKD', val) for val in conditional_words} | \
	{normalize('NFKC', val) for val in conditional_words}

	for word in file:
		num_conditional_words += 1 if word in conditional_words else 0
		num_characters += len(word)

	return num_conditional_words / num_characters

@textual_feature('words', 'ancient_greek')
def freq_personal_pronouns(file):
	num_pronouns = 0
	num_characters = 0
	personal_pronouns = {'ἐγώ', 'ἐγὼ', 'ἐμοῦ', 'μου', 'ἐμοί', 'ἐμοὶ', 'μοι', 'ἐμέ', 'ἐμὲ', 'με', 'ἡμεῖς', 'ἡμῶν', 
	'ἡμῖν', 'ἡμᾶς', 'σύ', 'σὺ', 'σοῦ', 'σου', 'σοί', 'σοὶ', 'σοι', 'σέ', 'σὲ', 'σε', 'ὑμεῖς', 'ὑμῶν', 'ὑμῖν', 'ὑμᾶς'}
	personal_pronouns = personal_pronouns | \
	{normalize('NFD', val) for val in personal_pronouns} | \
	{normalize('NFC', val) for val in personal_pronouns} | \
	{normalize('NFKD', val) for val in personal_pronouns} | \
	{normalize('NFKC', val) for val in personal_pronouns}

	for word in file:
		num_pronouns += 1 if word in personal_pronouns else 0
		num_characters += len(word)

	return num_pronouns / num_characters

@textual_feature('words', 'ancient_greek')
def freq_demonstrative(file):
	num_demonstratives = 0
	num_characters = 0
	demonstrative_pronouns = {'ἐκεῖνος', 'ἐκείνου', 'ἐκείνῳ', 'ἐκεῖνον', 'ἐκεῖνοι', 'ἐκείνων', 'ἐκείνοις', 'ἐκείνους', 
	'ἐκείνη', 'ἐκείνης', 'ἐκείνῃ', 'ἐκείνην', 'ἐκεῖναι', 'ἐκείναις', 'ἐκείνᾱς', 'ἐκείνας', 'ἐκεῖνο', 'ἐκεῖνα', 'ὅδε', 
	'τοῦδε', 'τῷδε', 'τόνδε', 'οἵδε', 'τῶνδε', 'τοῖσδε', 'τούσδε', 'ἥδε', 'τῆσδε', 'τῇδε', 'τήνδε', 'αἵδε', 'ταῖσδε', 
	'τᾱ́σδε', 'τάσδε', 'τόδε', 'τάδε', 'οὗτος', 'τούτου', 'τούτῳ', 'τοῦτον', 'οὗτοι', 'τούτων', 'τούτοις', 'τούτους', 
	'αὕτη', 'ταύτης', 'ταύτῃ', 'ταύτην', 'αὕται', 'ταύταις', 'ταύτᾱς', 'ταύτας', 'τοῦτο', 'ταῦτα'}
	demonstrative_pronouns = demonstrative_pronouns | \
	{normalize('NFD', val) for val in demonstrative_pronouns} | \
	{normalize('NFC', val) for val in demonstrative_pronouns} | \
	{normalize('NFKD', val) for val in demonstrative_pronouns} | \
	{normalize('NFKC', val) for val in demonstrative_pronouns}

	for word in file:
		num_demonstratives += 1 if word in demonstrative_pronouns else 0
		num_characters += len(word)

	return num_demonstratives / num_characters

@textual_feature('sentence_words', 'ancient_greek')
def freq_indefinite_pronoun_in_non_interrogative_sentence(file):
	num_indefinite_pronouns = 0
	num_characters = 0
	interrogative_chars = {';', ';'}
	pronoun_chars = {'τις', 'τινός', 'τινὸς', 'του', 'τινί', 'τινὶ', 'τῳ', 'τινά', 'τινὰ', 'τινές', 'τινὲς', 'τινῶν', 
	'τισί', 'τισὶ', 'τισίν', 'τισὶν', 'τινάς', 'τινὰς', 'τι'}
	pronoun_chars = pronoun_chars | \
	{normalize('NFD', val) for val in pronoun_chars} | \
	{normalize('NFC', val) for val in pronoun_chars} | \
	{normalize('NFKD', val) for val in pronoun_chars} | \
	{normalize('NFKC', val) for val in pronoun_chars}

	for line in file:
		if line[-1] not in interrogative_chars and len(line) > 1 and line[-2] not in interrogative_chars:
			for word in line:
				num_indefinite_pronouns += 1 if word in pronoun_chars else 0
				num_characters += len(word)

	return num_indefinite_pronouns / num_characters

@textual_feature('words', 'ancient_greek')
def freq_indefinite_pronoun_in_any_sentence(file):
	num_indefinite_pronouns = 0
	num_characters = 0
	pronoun_chars = {'τις', 'τινός', 'τινὸς', 'του', 'τινί', 'τινὶ', 'τῳ', 'τινά', 'τινὰ', 'τινές', 'τινὲς', 'τινῶν', 
	'τισί', 'τισὶ', 'τισίν', 'τισὶν', 'τινάς', 'τινὰς', 'τι'}
	pronoun_chars = pronoun_chars | \
	{normalize('NFD', val) for val in pronoun_chars} | \
	{normalize('NFC', val) for val in pronoun_chars} | \
	{normalize('NFKD', val) for val in pronoun_chars} | \
	{normalize('NFKC', val) for val in pronoun_chars}

	for word in file:
		num_indefinite_pronouns += 1 if word in pronoun_chars else 0
		num_characters += len(word)

	return num_indefinite_pronouns / num_characters

@textual_feature('words', 'ancient_greek')
def freq_allos(file):
	num_allos = 0
	num_characters = 0
	allos_characters = {'ἄλλος', 'ἄλλη', 'ἄλλο', 'ἄλλου', 'ἄλλῳ', 'ἄλλον', 'ἄλλοι', 'ἄλλων', 'ἄλλοις', 'ἄλλους', 
	'ἄλλης', 'ἄλλῃ', 'ἄλλην', 'ἄλλαι', 'ἄλλᾱς', 'ἄλλας', 'ἄλλα'}
	allos_characters = allos_characters | \
	{normalize('NFD', val) for val in allos_characters} | \
	{normalize('NFC', val) for val in allos_characters} | \
	{normalize('NFKD', val) for val in allos_characters} | \
	{normalize('NFKC', val) for val in allos_characters}

	for word in file:
		num_allos += 1 if word in allos_characters else 0
		num_characters += len(word)

	return num_allos / num_characters

@textual_feature('words', 'ancient_greek')
def freq_autos(file):
	num_autos = 0
	num_characters = 0
	autos_characters = {'αὐτός', 'αὐτὸς', 'αὐτοῦ', 'αὐτῷ', 'αὐτόν', 'αὐτὸν', 'αὐτοί', 'αὐτοὶ', 'αὐτῶν', 'αὐτοῖς', 
	'αὐτούς', 'αὐτοὺς', 'αὐτή', 'αὐτὴ', 'αὐτῆς', 'αὐτῇ', 'αὐτήν', 'αὐτὴν', 'αὐταί', 'αὐταὶ', 'αὐταῖς', 'αὐτᾱς', 
	'αὐτᾱ́ς', 'αὐτάς', 'αὐτὰς', 'αὐτό', 'αὐτὸ', 'αὐτά', 'αὐτὰ'}
	autos_characters = autos_characters | \
	{normalize('NFD', val) for val in autos_characters} | \
	{normalize('NFC', val) for val in autos_characters} | \
	{normalize('NFKD', val) for val in autos_characters} | \
	{normalize('NFKC', val) for val in autos_characters}

	for word in file:
		num_autos += 1 if word in autos_characters else 0
		num_characters += len(word)

	return num_autos / num_characters

@textual_feature('words', 'ancient_greek')
def freq_reflexive(file):
	num_reflexive = 0
	num_characters = 0

	reflexive_characters = {'ἐμαυτοῦ', 'ἐμαυτῷ', 'ἐμαυτόν', 'ἐμαυτὸν', 'ἐμαυτῆς', 'ἐμαυτῇ', 'ἐμαυτήν', 'ἐμαυτὴν', 
	'σεαυτοῦ', 'σεαυτῷ', 'σεαυτόν', 'σεαυτὸν', 'σεαυτῆς', 'σεαυτῇ', 'σεαυτήν', 'σεαυτὴν', 'ἑαυτοῦ', 'ἑαυτῷ', 'ἑαυτόν', 
	'ἑαυτὸν', 'ἑαυτῶν', 'ἑαυτοῖς', 'ἑαυτούς', 'ἑαυτοὺς', 'ἑαυτῆς', 'ἑαυτῇ', 'ἑαυτήν', 'ἑαυτὴν', 'ἑαυταῖς', 'ἑαυτάς', 
	'ἑαυτὰς', 'ἑαυτό', 'ἑαυτὸ', 'ἑαυτά', 'ἑαυτὰ'}
	reflexive_characters = reflexive_characters | \
	{normalize('NFD', val) for val in reflexive_characters} | \
	{normalize('NFC', val) for val in reflexive_characters} | \
	{normalize('NFKD', val) for val in reflexive_characters} | \
	{normalize('NFKC', val) for val in reflexive_characters}

	bigram_reflexive_characters = {'ἡμῶν': {'αὐτῶν'}, 'ἡμῖν': {'αὐτοῖς', 'αὐταῖς'}, 
	'ἡμᾶς': {'αὐτούς', 'αὐτοὺς', 'αὐτάς', 'αὐτὰς'}, 'ὑμῶν': {'αὐτῶν'}, 'ὑμῖν': {'αὐτοῖς', 'αὐταῖς'}, 
	'ὑμᾶς': {'αὐτούς', 'αὐτοὺς', 'αὐτάς', 'αὐτὰς'}, 'σφῶν': {'αὐτῶν'}, 'σφίσιν': {'αὐτοῖς', 'αὐταῖς'}, 
	'σφᾶς': {'αὐτούς', 'αὐτοὺς', 'αὐτάς', 'αὐτὰς'}}
	#This is just verbose syntax for normalizing all the keys and values in the dictionary with NFD, NFC, NFKD, & NFKC
	#The double star (**) unpacking is how dictionaries are merged https://stackoverflow.com/a/26853961/7102572
	bigram_reflexive_characters = {**bigram_reflexive_characters, 
	**{normalize('NFD', key): {normalize('NFD', v) for v in val} for key, val in bigram_reflexive_characters.items()}, 
	**{normalize('NFC', key): {normalize('NFC', v) for v in val} for key, val in bigram_reflexive_characters.items()}, 
	**{normalize('NFKD', key): {normalize('NFKD', v) for v in val} for key, val in bigram_reflexive_characters.items()}, 
	**{normalize('NFKC', key): {normalize('NFKC', v) for v in val} for key, val in bigram_reflexive_characters.items()}}

	bigram_first_half = None
	for word in file:

		#Found monogram characters
		if word in reflexive_characters:
			num_reflexive += 1
			bigram_first_half = None

		#Found the first part of the reflexive bigram
		elif word in bigram_reflexive_characters:
			bigram_first_half = word

		#Found the second part of the reflexive bigram
		elif bigram_first_half in bigram_reflexive_characters and word in bigram_reflexive_characters[bigram_first_half]:
			num_reflexive += 2
			bigram_first_half = None

		#Default case
		else:
			bigram_first_half = None

		num_characters += len(word)

	return num_reflexive / num_characters

@textual_feature('sentence_words', 'ancient_greek')
def freq_vocative_sentences(file):
	num_vocatives = 0
	vocative_characters = {'ὦ'}
	vocative_characters = vocative_characters | \
	{normalize('NFD', val) for val in vocative_characters} | \
	{normalize('NFC', val) for val in vocative_characters} | \
	{normalize('NFKD', val) for val in vocative_characters} | \
	{normalize('NFKC', val) for val in vocative_characters}

	for line in file:
		for word in line:
			if word in vocative_characters:
				num_vocatives += 1
				break

	return num_vocatives / len(file)

@textual_feature('words', 'ancient_greek')
def freq_superlative(file):
	num_superlative = 0
	num_characters = 0
	superlative_ending_characters = ['τατος', 'τάτου', 'τάτῳ', 'τατον', 'τατοι', 'τάτων', 
	'τάτοις', 'τάτους', 'τάτη', 'τάτης', 'τάτῃ', 'τάτην', 'ταται', 
	'τάταις', 'τάτας', 'τατα']
	#The endswith() method requires a tuple
	superlative_ending_characters = tuple(superlative_ending_characters + \
	[normalize('NFD', val) for val in superlative_ending_characters] + \
	[normalize('NFC', val) for val in superlative_ending_characters] + \
	[normalize('NFKD', val) for val in superlative_ending_characters] + \
	[normalize('NFKC', val) for val in superlative_ending_characters])

	for word in file:
		num_superlative += 1 if word.endswith(superlative_ending_characters) else 0
		num_characters += len(word)

	return num_superlative / num_characters

@textual_feature('words', 'ancient_greek')
def freq_conjunction(file):
	num_conjunction = 0
	num_characters = 0
	conjunction_chars = {'τε', 'καί', 'καὶ', 'δέ', 'δὲ', 'ἀλλά', 'ἀλλὰ', 'καίτοι', 'οὐδέ', 'οὐδὲ', 'μηδέ', 'μηδὲ', 'ἤ', 'ἢ'}
	conjunction_chars = conjunction_chars | \
	{normalize('NFD', val) for val in conjunction_chars} | \
	{normalize('NFC', val) for val in conjunction_chars} | \
	{normalize('NFKD', val) for val in conjunction_chars} | \
	{normalize('NFKC', val) for val in conjunction_chars}

	for word in file:
		num_conjunction += 1 if word in conjunction_chars else 0
		num_characters += len(word)

	return num_conjunction / num_characters

@textual_feature('sentence_words', 'ancient_greek')
def mean_sentence_length(file):
	return reduce(lambda cur_len, line: cur_len + 
		reduce(lambda word_len, word: word_len + len(word), line, 0), file, 0) / len(file)

@textual_feature('sentence_words', 'ancient_greek')
def non_interrogative_sentence_with_relative_clause(file):
	num_sentence_with_clause = 0
	num_non_interrogative_sentence = 0
	interrogative_chars = {';', ';'} #Second character is Greek semi colon
	pronouns = {'ὅς', 'ὃς', 'οὗ', 'ᾧ', 'ὅν', 'ὃν', 'οἵ', 'οἳ', 'ὧν', 'οἷς', 'οὕς', 'οὓς', 'ἥ', 'ἣ', 'ἧς', 'ᾗ', 
	'ἥν', 'ἣν', 'αἵ', 'αἳ', 'αἷς', 'ἅς', 'ἃς', 'ὅ', 'ὃ', 'ἅ', 'ἃ'}
	pronouns = pronouns | \
	{normalize('NFD', val) for val in pronouns} | \
	{normalize('NFC', val) for val in pronouns} | \
	{normalize('NFKD', val) for val in pronouns} | \
	{normalize('NFKC', val) for val in pronouns}

	for line in file:
		if line[-1] not in interrogative_chars and len(line) > 1 and line[-2] not in interrogative_chars:
			for word in line:
				if word in pronouns:
					num_sentence_with_clause += 1
					break
			num_non_interrogative_sentence += 1

	return num_sentence_with_clause / num_non_interrogative_sentence

@textual_feature('words', 'ancient_greek')
def mean_length_relative_clause(file):
	num_relative_clause = 0
	sum_length_relative_clause = 0
	pronouns = {'ὅς', 'ὃς', 'οὗ', 'ᾧ', 'ὅν', 'ὃν', 'οἵ', 'οἳ', 'ὧν', 'οἷς', 'οὕς', 'οὓς', 'ἥ', 'ἣ', 'ἧς', 'ᾗ', 
	'ἥν', 'ἣν', 'αἵ', 'αἳ', 'αἷς', 'ἅς', 'ἃς', 'ὅ', 'ὃ', 'ἅ', 'ἃ'}
	pronouns = pronouns | \
	{normalize('NFD', val) for val in pronouns} | \
	{normalize('NFC', val) for val in pronouns} | \
	{normalize('NFKD', val) for val in pronouns} | \
	{normalize('NFKC', val) for val in pronouns}
	punctuation = {'.', ',', ':', ';', ';'}
	punctuation = punctuation | \
	{normalize('NFD', val) for val in punctuation} | \
	{normalize('NFC', val) for val in punctuation} | \
	{normalize('NFKD', val) for val in punctuation} | \
	{normalize('NFKC', val) for val in punctuation}

	in_relative_clause = False

	for word in file:
		if word in punctuation:
			in_relative_clause = False
		elif word in pronouns:
			in_relative_clause = True
			num_relative_clause += 1
		if in_relative_clause:
			sum_length_relative_clause += len(word)

	return 0 if num_relative_clause == 0 else sum_length_relative_clause / num_relative_clause

#Count of relative pronouns in non-interrogative sentences / total non-interrogative sentences
@textual_feature('sentence_words', 'ancient_greek')
def relative_clause_per_non_interrogative_sentence(file):
	num_relative_pronoun = 0
	num_non_interrogative_sentence = 0
	interrogative_chars = {';', ';'} #Second character is Greek semi colon
	pronouns = {'ὅς', 'ὃς', 'οὗ', 'ᾧ', 'ὅν', 'ὃν', 'οἵ', 'οἳ', 'ὧν', 'οἷς', 'οὕς', 'οὓς', 'ἥ', 'ἣ', 'ἧς', 'ᾗ', 
	'ἥν', 'ἣν', 'αἵ', 'αἳ', 'αἷς', 'ἅς', 'ἃς', 'ὅ', 'ὃ', 'ἅ', 'ἃ'}
	pronouns = pronouns | \
	{normalize('NFD', val) for val in pronouns} | \
	{normalize('NFC', val) for val in pronouns} | \
	{normalize('NFKD', val) for val in pronouns} | \
	{normalize('NFKC', val) for val in pronouns}

	for line in file:
		if line[-1] not in interrogative_chars and len(line) > 1 and line[-2] not in interrogative_chars:
			for word in line:
				num_relative_pronoun += 1 if word in pronouns else 0
			num_non_interrogative_sentence += 1

	return num_relative_pronoun / num_non_interrogative_sentence

#Count of all standalone instances of ἔπειτα, ὅμως, καίπερ, ἅτε, οἷα
@textual_feature('words', 'ancient_greek')
def freq_circumstantial_participial_clauses(file):
	num_participles = 0
	num_characters = 0
	participles = {'ἔπειτα', 'ὅμως', 'καίπερ', 'ἅτε', 'οἷα'}
	participles = participles | \
	{normalize('NFD', val) for val in participles} | \
	{normalize('NFC', val) for val in participles} | \
	{normalize('NFKD', val) for val in participles} | \
	{normalize('NFKC', val) for val in participles}

	for word in file:
		num_participles += 1 if word in participles else 0
		num_characters += len(word)

	return num_participles / num_characters

@textual_feature('words', 'ancient_greek')
def freq_purpose_clause(file):
	num_purpose_words = 0
	num_characters = 0
	purpose_characters = {'ἵνα', 'ὅπως'}
	purpose_characters = purpose_characters | \
	{normalize('NFD', val) for val in purpose_characters} | \
	{normalize('NFC', val) for val in purpose_characters} | \
	{normalize('NFKD', val) for val in purpose_characters} | \
	{normalize('NFKC', val) for val in purpose_characters}

	for word in file:
		num_purpose_words += 1 if word in purpose_characters else 0
		num_characters += len(word)

	return num_purpose_words / num_characters

@textual_feature('words', 'ancient_greek')
def freq_ws(file):
	num_ws = 0
	num_characters = 0
	ws_characters = {'ὡς'}
	ws_characters = ws_characters | \
	{normalize('NFD', val) for val in ws_characters} | \
	{normalize('NFC', val) for val in ws_characters} | \
	{normalize('NFKD', val) for val in ws_characters} | \
	{normalize('NFKC', val) for val in ws_characters}

	for word in file:
		num_ws += 1 if word in ws_characters else 0
		num_characters += len(word)

	return num_ws / num_characters

# Bad feature when result is NaN or infinity
# @textual_feature('words', 'ancient_greek')
# def ratio_ina_to_opos(file):
# 	num_ina = 0
# 	num_opos = 0
# 	ina_chars = {'ἵνα'}
# 	ina_chars = ina_chars | \
# 	{normalize('NFD', val) for val in ina_chars} | \
# 	{normalize('NFC', val) for val in ina_chars} | \
# 	{normalize('NFKD', val) for val in ina_chars} | \
# 	{normalize('NFKC', val) for val in ina_chars}
# 	opos_chars = {'ὅπως'}
# 	opos_chars = opos_chars | \
# 	{normalize('NFD', val) for val in opos_chars} | \
# 	{normalize('NFC', val) for val in opos_chars} | \
# 	{normalize('NFKD', val) for val in opos_chars} | \
# 	{normalize('NFKC', val) for val in opos_chars}

# 	for word in file:
# 		if word in ina_chars:
# 			num_ina += 1
# 		elif word in opos_chars:
# 			num_opos += 1

# 	return math.nan if num_ina == 0 and num_opos == 0 else math.inf if num_opos == 0 else num_ina / num_opos

@textual_feature('words', 'ancient_greek')
def freq_wste_not_preceded_by_eta(file):
	num_wste = 0
	num_characters = 0
	wste_characters = {'ὥστε'}
	wste_characters = wste_characters | \
	{normalize('NFD', val) for val in wste_characters} | \
	{normalize('NFC', val) for val in wste_characters} | \
	{normalize('NFKD', val) for val in wste_characters} | \
	{normalize('NFKC', val) for val in wste_characters}
	eta_chars = {'ἤ', 'ἢ'}
	eta_chars = eta_chars | \
	{normalize('NFD', val) for val in eta_chars} | \
	{normalize('NFC', val) for val in eta_chars} | \
	{normalize('NFKD', val) for val in eta_chars} | \
	{normalize('NFKC', val) for val in eta_chars}
	ok_to_add = True

	for word in file:
		num_wste += 1 if word in wste_characters and ok_to_add else 0
		num_characters += len(word)
		ok_to_add = word not in eta_chars

	return num_wste / num_characters

# Only 54 matches across 42 files for regex "(ἤ|ἢ) (\w+ )*?ὥστε" and 33 matches across 27 files for "(ἤ|ἢ) ὥστε"
# @textual_feature('words', 'ancient_greek')
# def freq_wste_preceded_by_eta(file):
# 	num_wste_characters = 0
# 	num_characters = 0
# 	wste_characters = {'ὥστε'}
# 	wste_characters = wste_characters | \
# 	{normalize('NFD', val) for val in wste_characters} | \
# 	{normalize('NFC', val) for val in wste_characters} | \
# 	{normalize('NFKD', val) for val in wste_characters} | \
# 	{normalize('NFKC', val) for val in wste_characters}
# 	eta_chars = {'ἤ', 'ἢ'}
# 	eta_chars = eta_chars | \
# 	{normalize('NFD', val) for val in eta_chars} | \
# 	{normalize('NFC', val) for val in eta_chars} | \
# 	{normalize('NFKD', val) for val in eta_chars} | \
# 	{normalize('NFKC', val) for val in eta_chars}
# 	ok_to_add = False

# 	for word in file:
# 		num_wste_characters += len(word) if word in wste_characters and ok_to_add else 0
# 		num_characters += len(word)
# 		ok_to_add = word in eta_chars

# 	return num_wste_characters / num_characters

@textual_feature('words', 'ancient_greek')
def freq_temporal_and_causal_clauses(file):
	num_clause_words = 0
	num_characters = 0
	clause_chars = {'μέϰρι', 'ἕως', 'πρίν', 'πρὶν', 'ἐπεί', 'ἐπεὶ', 'ἐπειδή', 'ἐπειδὴ', 'ἐπειδάν', 'ἐπειδὰν', 'ὅτε', 'ὅταν'}
	clause_chars = clause_chars | \
	{normalize('NFD', val) for val in clause_chars} | \
	{normalize('NFC', val) for val in clause_chars} | \
	{normalize('NFKD', val) for val in clause_chars} | \
	{normalize('NFKC', val) for val in clause_chars}

	for word in file:
		num_clause_words += 1 if word in clause_chars else 0
		num_characters += len(word)

	return num_clause_words / num_characters

@textual_feature('sentence_words', 'ancient_greek')
def variance_of_sentence_length(file):
	num_sentences = 0
	total_len = 0

	for line in file:
		num_sentences += 1
		total_len += reduce(lambda cur_len, word: cur_len + len(word), line, 0)
	mean = total_len / num_sentences
	squared_difference = 0
	for line in file:
		squared_difference += (reduce(lambda cur_len, word: cur_len + len(word), line, 0) - mean) ** 2

	return squared_difference / num_sentences

@textual_feature('words', 'ancient_greek')
def particles_per_sentence(file):
	num_particles = 0
	#Word tokenizer doesn't work well with ellision - apostrophes are removed
	particles = {'ἄν', 'ἂν', 'ἆρα', 'γε', "γ", "δ", 'δέ', 'δὲ', 'δή', 'δὴ', 'ἕως', "κ", 'κε', 'κέ', 'κὲ', 'κέν', 'κὲν', 
	'κεν', 'μά', 'μὰ' 'μέν', 'μὲν', 'μέντοι', 'μή', 'μὴ', 'μήν', 'μὴν', 'μῶν', 'νύ', 'νὺ', 'νυ', 'οὐ', 'οὔ', 'οὒ', 'οὖν', 
	'περ', 'πω', "τ", 'τε', 'τοι'}
	particles = particles | \
	{normalize('NFD', val) for val in particles} | \
	{normalize('NFC', val) for val in particles} | \
	{normalize('NFKD', val) for val in particles} | \
	{normalize('NFKC', val) for val in particles}

	for word in file:
		num_particles += 1 if word in particles else 0

	num_sentences = file.count('.') + file.count(';') + file.count(';') #Greek semi colon
	return num_particles / num_sentences

# No interpunct symbols found in the entire tesserae corpus - searched with regex: (·|·|∙|⋅|•|᛫|‧|⦁|⸳|・|ꞏ|･|𐄁)
# @textual_feature('default', 'ancient_greek')
# def freq_raised_dot(file):
# 	#Unicode from https://en.wikipedia.org/wiki/Interpunct#Similar_symbols
# 	#'\u00B7' is '·', '\u0387' is '·', '\u2219' is '∙', '\u22C5' is '⋅', '\u2022' is '•', '\u16EB' is '᛫', '\u2027' is '‧', 
# 	#'\u2981' is '⦁', '\u2E33' is '⸳', '\u30FB' is '・', '\uA78F' is 'ꞏ', '\uFF65' is '･', '\U00010101' is '𐄁'
# 	dot_chars = {'·', '·', '∙', '⋅', '•', '᛫', '‧', '⦁', '⸳', '・', 'ꞏ', '･', '𐄁'}
# 	num_dot_chars = 0
# 	for char in file:
# 		num_dot_chars += 1 if char in dot_chars else 0
# 	return num_dot_chars / len(file)

@textual_feature('words', 'ancient_greek')
def freq_men(file):
	num_men = 0
	num_characters = 0
	men_chars = {'μέν', 'μὲν'}
	men_chars = men_chars | \
	{normalize('NFD', val) for val in men_chars} | \
	{normalize('NFC', val) for val in men_chars} | \
	{normalize('NFKD', val) for val in men_chars} | \
	{normalize('NFKC', val) for val in men_chars}

	for word in file:
		num_men += 1 if word in men_chars else 0
		num_characters += len(word)
	return num_men / num_characters

#These files are composites of files that already exist in parts
composite_files_to_exclude = {
	'tesserae/texts/grc/antiphon.speeches.tess',
	'tesserae/texts/grc/apollonius.argonautica.tess',
	'tesserae/texts/grc/appian.civil_wars.tess',
	'tesserae/texts/grc/dionysius_halicarnassensis.antiquitates_romanae.tess',
	'tesserae/texts/grc/eusebius_caesarea.historia_ecclesiastica.tess',
	'tesserae/texts/grc/flavius_josephus.antiquitates_judaicae.tess',
	'tesserae/texts/grc/flavius_josephus.contra_apionem.tess',
	'tesserae/texts/grc/flavius_josephus.de_bello_judaico_libri_vii.tess',
	'tesserae/texts/grc/galen.natural_faculties.tess',
	'tesserae/texts/grc/herodotus.histories.tess',
	'tesserae/texts/grc/homer.iliad.tess',
	'tesserae/texts/grc/homer.odyssey.tess',
	'tesserae/texts/grc/hyperides.speeches.tess',
	'tesserae/texts/grc/isaeus.speeches.tess',
	'tesserae/texts/grc/isocrates.letters.tess',
	'tesserae/texts/grc/isocrates.speeches.tess',
	'tesserae/texts/grc/lysias.speeches.tess',
	'tesserae/texts/grc/nonnus_of_panopolis.dionysiaca.tess',
	'tesserae/texts/grc/oppian.halieutica.tess',
	'tesserae/texts/grc/oppian_of_apamea.cynegetica.tess',
	'tesserae/texts/grc/pausanias.description_of_greece.tess',
	'tesserae/texts/grc/philostratus_the_athenian.vita_apollonii.tess',
	'tesserae/texts/grc/pindar.odes.tess',
	'tesserae/texts/grc/plato.epistles.tess',
	'tesserae/texts/grc/plato.leges.tess',
	'tesserae/texts/grc/plato.respublica.tess',
	'tesserae/texts/grc/quintus_smyrnaeus.fall_of_troy.tess',
	'tesserae/texts/grc/strabo.geography.tess',
	'tesserae/texts/grc/thucydides.peleponnesian_war.tess',
}

if __name__ == '__main__':

	#Download corpus if non-existent
	corpus_dir = join('tesserae', 'texts', 'grc')
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
		excluded_paths=composite_files_to_exclude,

		#Only extract the following features
		# features=['freq_men'], 

		#Output the results to a file in order to be processed by machine learning algorithms
		output_file=None if len(sys.argv) <= 1 else sys.argv[1] 
	)
