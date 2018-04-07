# -*- coding: utf-8 -*-

import os
import sys
import math
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from cltk.stem.lemma import LemmaReplacer
from unicodedata import normalize #the cltk_normalize cannot decompose (only has NFC & NFKC, not NFD or NFKD)
#Reference: https://jktauber.com/articles/python-unicode-ancient-greek/

class Features:
	def freq_interrogatives(file):
		file = TokenizeSentence("greek").tokenize_sentences(file)
		num_interrogative = 0

		for line in file:
			num_interrogative += line.count(';') + line.count(';')

		return num_interrogative / len(file)

	def freq_conditional_characters(file):
		file = WordTokenizer('greek').tokenize(file)
		num_conditional_characters = 0
		num_characters = 0
		conditional_characters = {'εἰ', 'εἴ', 'εἲ', 'ἐάν', 'ἐὰν'}
		conditional_characters = conditional_characters | \
		{normalize('NFD', val) for val in conditional_characters} | \
		{normalize('NFC', val) for val in conditional_characters} | \
		{normalize('NFKD', val) for val in conditional_characters} | \
		{normalize('NFKC', val) for val in conditional_characters}

		for word in file:
			num_conditional_characters += len(word) if word in conditional_characters else 0
			num_characters += len(word)

		return num_conditional_characters / num_characters

	def freq_personal_pronouns(file):
		file = WordTokenizer('greek').tokenize(file)
		num_pronouns = 0
		num_characters = 0
		personal_pronouns = {'ἐγώ', 'ἐγὼ', 'ἐμοῦ', 'μου', 'ἐμοί', 'ἐμοὶ', 'μοι', 'ἐμέ', 'ἐμὲ', 'με', 'ἡμεῖς', 'ἡμῶν', \
		'ἡμῖν', 'ἡμᾶς', 'σύ', 'σὺ', 'σοῦ', 'σου', 'σοί', 'σοὶ', 'σοι', 'σέ', 'σὲ', 'σε', 'ὑμεῖς', 'ὑμῶν', 'ὑμῖν', 'ὑμᾶς'}
		personal_pronouns = personal_pronouns | \
		{normalize('NFD', val) for val in personal_pronouns} | \
		{normalize('NFC', val) for val in personal_pronouns} | \
		{normalize('NFKD', val) for val in personal_pronouns} | \
		{normalize('NFKC', val) for val in personal_pronouns}

		for word in file:
			num_pronouns += len(word) if word in personal_pronouns else 0
			num_characters += len(word)

		return num_pronouns / num_characters

	def freq_demonstrative(file):
		file = WordTokenizer('greek').tokenize(file)
		num_demonstratives_characters = 0
		num_characters = 0
		demonstrative_pronouns = {'ἐκεῖνος', 'ἐκείνου', 'ἐκείνῳ', 'ἐκεῖνον', 'ἐκεῖνοι', 'ἐκείνων', 'ἐκείνοις', 'ἐκείνους', \
		'ἐκείνη', 'ἐκείνης', 'ἐκείνῃ', 'ἐκείνην', 'ἐκεῖναι', 'ἐκείναις', 'ἐκείνᾱς', 'ἐκείνας', 'ἐκεῖνο', 'ἐκεῖνα', 'ὅδε', \
		'τοῦδε', 'τῷδε', 'τόνδε', 'οἵδε', 'τῶνδε', 'τοῖσδε', 'τούσδε', 'ἥδε', 'τῆσδε', 'τῇδε', 'τήνδε', 'αἵδε', 'ταῖσδε', \
		'τᾱ́σδε', 'τάσδε', 'τόδε', 'τάδε', 'οὗτος', 'τούτου', 'τούτῳ', 'τοῦτον', 'οὗτοι', 'τούτων', 'τούτοις', 'τούτους', \
		'αὕτη', 'ταύτης', 'ταύτῃ', 'ταύτην', 'αὕται', 'ταύταις', 'ταύτᾱς', 'ταύτας', 'τοῦτο', 'ταῦτα'}
		demonstrative_pronouns = demonstrative_pronouns | \
		{normalize('NFD', val) for val in demonstrative_pronouns} | \
		{normalize('NFC', val) for val in demonstrative_pronouns} | \
		{normalize('NFKD', val) for val in demonstrative_pronouns} | \
		{normalize('NFKC', val) for val in demonstrative_pronouns}

		for word in file:
			num_demonstratives_characters += len(word) if word in demonstrative_pronouns else 0
			num_characters += len(word)

		return num_demonstratives_characters / num_characters

	def freq_indefinite_pronoun_in_non_interrogative_sentence(file):
		file = TokenizeSentence("greek").tokenize_sentences(file)
		num_indefinite_pronoun_chars = 0
		num_characters = 0
		interrogative_chars = {';', ';'}
		pronoun_chars = {'τις', 'τινός', 'τινὸς', 'του', 'τινί', 'τινὶ', 'τῳ', 'τινά', 'τινὰ', 'τινές', 'τινὲς', 'τινῶν', \
		'τισί', 'τισὶ', 'τισίν', 'τισὶν', 'τινάς', 'τινὰς', 'τι'}
		pronoun_chars = pronoun_chars | \
		{normalize('NFD', val) for val in pronoun_chars} | \
		{normalize('NFC', val) for val in pronoun_chars} | \
		{normalize('NFKD', val) for val in pronoun_chars} | \
		{normalize('NFKC', val) for val in pronoun_chars}

		for line in file:
			if line[-1] not in interrogative_chars:
				line = WordTokenizer('greek').tokenize(line)
				for word in line:
					num_indefinite_pronoun_chars += len(word) if word in pronoun_chars else 0
					num_characters += len(word)

		return num_indefinite_pronoun_chars / num_characters

	def freq_allos(file):
		file = WordTokenizer('greek').tokenize(file)
		num_allos = 0
		num_characters = 0
		allos_characters = {'ἄλλος', 'ἄλλη', 'ἄλλο', 'ἄλλου', 'ἄλλῳ', 'ἄλλον', 'ἄλλοι', 'ἄλλων', 'ἄλλοις', 'ἄλλους', \
		'ἄλλης', 'ἄλλῃ', 'ἄλλην', 'ἄλλαι', 'ἄλλᾱς', 'ἄλλας', 'ἄλλα'}
		allos_characters = allos_characters | \
		{normalize('NFD', val) for val in allos_characters} | \
		{normalize('NFC', val) for val in allos_characters} | \
		{normalize('NFKD', val) for val in allos_characters} | \
		{normalize('NFKC', val) for val in allos_characters}

		for word in file:
			num_allos += len(word) if word in allos_characters else 0
			num_characters += len(word)

		return num_allos / num_characters

	def freq_autos(file):
		file = WordTokenizer('greek').tokenize(file)
		num_autos = 0
		num_characters = 0
		autos_characters = {'αὐτός', 'αὐτὸς', 'αὐτοῦ', 'αὐτῷ', 'αὐτόν', 'αὐτὸν', 'αὐτοί', 'αὐτοὶ', 'αὐτῶν', 'αὐτοῖς', \
		'αὐτούς', 'αὐτοὺς', 'αὐτή', 'αὐτὴ', 'αὐτῆς', 'αὐτῇ', 'αὐτήν', 'αὐτὴν', 'αὐταί', 'αὐταὶ', 'αὐταῖς', 'αὐτᾱς', \
		'αὐτᾱ́ς', 'αὐτάς', 'αὐτὰς', 'αὐτό', 'αὐτὸ', 'αὐτά', 'αὐτὰ'}
		autos_characters = autos_characters | \
		{normalize('NFD', val) for val in autos_characters} | \
		{normalize('NFC', val) for val in autos_characters} | \
		{normalize('NFKD', val) for val in autos_characters} | \
		{normalize('NFKC', val) for val in autos_characters}

		for word in file:
			num_autos += len(word) if word in autos_characters else 0
			num_characters += len(word)

		return num_autos / num_characters

	def freq_reflexive(file):
		file = WordTokenizer('greek').tokenize(file)
		num_reflexive = 0
		num_characters = 0

		reflexive_characters = {'ἐμαυτοῦ', 'ἐμαυτῷ', 'ἐμαυτόν', 'ἐμαυτὸν', 'ἐμαυτῆς', 'ἐμαυτῇ', 'ἐμαυτήν', 'ἐμαυτὴν', \
		'σεαυτοῦ', 'σεαυτῷ', 'σεαυτόν', 'σεαυτὸν', 'σεαυτῆς', 'σεαυτῇ', 'σεαυτήν', 'σεαυτὴν', 'ἑαυτοῦ', 'ἑαυτῷ', 'ἑαυτόν', \
		'ἑαυτὸν', 'ἑαυτῶν', 'ἑαυτοῖς', 'ἑαυτούς', 'ἑαυτοὺς', 'ἑαυτῆς', 'ἑαυτῇ', 'ἑαυτήν', 'ἑαυτὴν', 'ἑαυταῖς', 'ἑαυτάς', \
		'ἑαυτὰς', 'ἑαυτό', 'ἑαυτὸ', 'ἑαυτά', 'ἑαυτὰ'}
		reflexive_characters = reflexive_characters | \
		{normalize('NFD', val) for val in reflexive_characters} | \
		{normalize('NFC', val) for val in reflexive_characters} | \
		{normalize('NFKD', val) for val in reflexive_characters} | \
		{normalize('NFKC', val) for val in reflexive_characters}

		bigram_reflexive_characters = {'ἡμῶν': {'αὐτῶν'}, 'ἡμῖν': {'αὐτοῖς', 'αὐταῖς'}, \
		'ἡμᾶς': {'αὐτούς', 'αὐτοὺς', 'αὐτάς', 'αὐτὰς'}, 'ὑμῶν': {'αὐτῶν'}, 'ὑμῖν': {'αὐτοῖς', 'αὐταῖς'}, \
		'ὑμᾶς': {'αὐτούς', 'αὐτοὺς', 'αὐτάς', 'αὐτὰς'}, 'σφῶν': {'αὐτῶν'}, 'σφίσιν': {'αὐτοῖς', 'αὐταῖς'}, \
		'σφᾶς': {'αὐτούς', 'αὐτοὺς', 'αὐτάς', 'αὐτὰς'}}
		#This is just verbose syntax for normalizing all the keys and values in the dictionary with NFD, NFC, NFKD, & NFKC
		#The double star (**) unpacking is how dictionaries are merged https://stackoverflow.com/a/26853961/7102572
		bigram_reflexive_characters = {**bigram_reflexive_characters, \
		**{normalize('NFD', key): {normalize('NFD', v) for v in val} for key, val in bigram_reflexive_characters.items()}, \
		**{normalize('NFC', key): {normalize('NFC', v) for v in val} for key, val in bigram_reflexive_characters.items()}, \
		**{normalize('NFKD', key): {normalize('NFKD', v) for v in val} for key, val in bigram_reflexive_characters.items()}, \
		**{normalize('NFKC', key): {normalize('NFKC', v) for v in val} for key, val in bigram_reflexive_characters.items()}}

		bigram_first_half = None
		for word in file:

			#Found monogram characters
			if word in reflexive_characters:
				num_reflexive += len(word)
				bigram_first_half = None

			#Found the first part of the reflexive bigram
			elif word in bigram_reflexive_characters:
				bigram_first_half = word

			#Found the second part of the reflexive bigram
			elif bigram_first_half in bigram_reflexive_characters and word in bigram_reflexive_characters[bigram_first_half]:
				num_reflexive += len(bigram_first_half) + len(word)
				bigram_first_half = None

			#Default case
			else:
				bigram_first_half = None

			num_characters += len(word)

		return num_reflexive / num_characters

	def freq_vocative_sentences(file):
		file = TokenizeSentence("greek").tokenize_sentences(file)
		num_vocative = 0

		for line in file:
			num_vocative += 1 if 'ὦ' in line else 0

		return num_vocative / len(file)

	def freq_superlative(file):
		file = WordTokenizer('greek').tokenize(file)
		num_superlative = 0
		num_characters = 0

		for word in file:
			num_superlative += len(word) if word.endswith(('τατος', 'τάτου', 'τάτῳ', 'τατον', 'τατοι', 'τάτων', \
				'τάτοις', 'τάτους', 'τάτη', 'τάτης', 'τάτῃ', 'τάτην', 'ταται', 'τάταις', 'τάτας', 'τατα')) else 0
			num_characters += len(word)

		return num_superlative / num_characters

	def freq_conjunction(file):
		file = WordTokenizer('greek').tokenize(file)
		num_conjunction = 0
		num_characters = 0

		for word in file:
			num_conjunction += len(word) if word in {'τε', 'καί', 'δέ', 'ἀλλά', 'καίτοι', 'οὐδέ', 'μηδέ', 'ἤ'} else 0
			num_characters += len(word)

		return num_conjunction / num_characters

	def mean_sentence_length(file):
		file = TokenizeSentence("greek").tokenize_sentences(file)
		lens = 0

		for line in file:
			lens += len(line)

		return lens / len(file)

	def non_interoggative_sentence_with_relative_clause(file):
		file = TokenizeSentence("greek").tokenize_sentences(file)
		num_sentence_with_clause = 0
		num_non_interrogative_sentence = 0
		interrogative_chars = {';', ';'} #Second character is Greek semi colon
		pronouns = {'ὅς', 'ὃς', 'οὗ', 'ᾧ', 'ὅν', 'ὃν', 'οἵ', 'οἳ', 'ὧν', 'οἷς', 'οὕς', 'οὓς', 'ἥ', 'ἣ', 'ᾗς', \
		'ἥν', 'ἣν', 'αἵ', 'αἳ', 'αἷς', 'ἅς', 'ἃς', 'ὅ', 'ὃ', 'ἅ', 'ἃ'}
		pronouns = pronouns | \
		{normalize('NFD', val) for val in pronouns} | \
		{normalize('NFC', val) for val in pronouns} | \
		{normalize('NFKD', val) for val in pronouns} | \
		{normalize('NFKC', val) for val in pronouns}

		for line in file:
			if line[-1] not in interrogative_chars:
				line = WordTokenizer('greek').tokenize(line)
				for word in line:
					if word in pronouns:
						num_sentence_with_clause += 1
						break
				num_non_interrogative_sentence += 1

		return num_sentence_with_clause / num_non_interrogative_sentence

	# Omit for now
	# def mean_length_relative_clause(file):
	# 	return 0

	#Count of relative pronouns in non-interrogative sentences / total non-interrogative sentences
	def relative_clause_per_sentence(file):
		file = TokenizeSentence("greek").tokenize_sentences(file)
		num_relative_pronoun = 0
		num_non_interrogative_sentence = 0
		pronouns = {'ὅς', 'ὃς', 'οὗ', 'ᾧ', 'ὅν', 'ὃν', 'οἵ', 'οἳ', 'ὧν', 'οἷς', 'οὕς', 'οὓς', 'ἥ', 'ἣ', 'ᾗς', \
		'ἥν', 'ἣν', 'αἵ', 'αἳ', 'αἷς', 'ἅς', 'ἃς', 'ὅ', 'ὃ', 'ἅ', 'ἃ'}
		pronouns = pronouns | \
		{normalize('NFD', val) for val in pronouns} | \
		{normalize('NFC', val) for val in pronouns} | \
		{normalize('NFKD', val) for val in pronouns} | \
		{normalize('NFKC', val) for val in pronouns}

		for line in file:
			if not line.endswith(';'): #TODO what if line ends in quote or bracket?
				for word in line.split():
					num_relative_pronoun += 1 if word in pronouns else 0
				num_non_interrogative_sentence += 1

		return num_relative_pronoun / num_non_interrogative_sentence

	#Count of all standalone instances of ἔπειτα, ὅμως, καίπερ, ἅτε, οἷα
	def freq_circumstantial_participial_clauses(file):
		file = WordTokenizer('greek').tokenize(file)
		num_participles_characters = 0
		num_characters = 0
		participles = {'ἔπειτα', 'ὅμως', 'καίπερ', 'ἅτε', 'οἷα'}

		for word in file:
			num_participles_characters += len(word) if word in participles else 0
			num_characters += len(word)

		return num_participles_characters / num_characters

	def freq_purpose_clause(file):
		file = WordTokenizer('greek').tokenize(file)
		num_purpose_characters = 0
		num_characters = 0
		purpose_characters = {'ἵνα', 'ὃπως'}

		for word in file:
			num_purpose_characters += len(word) if word in purpose_characters else 0
			num_characters += len(word)

		return num_purpose_characters / num_characters

	def freq_ws(file):
		file = WordTokenizer('greek').tokenize(file)
		num_ws_characters = 0
		num_characters = 0
		ws_characters = 'ὡς'

		for word in file:
			num_ws_characters += len(word) if word == ws_characters else 0
			num_characters += len(word)

		return num_ws_characters / num_characters

	def ratio_ina_to_opos(file):
		file = WordTokenizer('greek').tokenize(file)
		num_ina = 0
		num_opos = 0

		for word in file:
			if word == 'ἵνα':
				num_ina += 1
			elif word == 'ὃπως':
				num_opos += 1

		return math.nan if num_ina == 0 and num_opos == 0 else math.inf if num_opos == 0 else num_ina / num_opos

	def freq_wste_not_precceded_by_eta(file):
		file = WordTokenizer('greek').tokenize(file)
		num_wste_characters = 0
		num_characters = 0
		wste_characters = 'ὥστε'
		ok_to_add = True

		for word in file:
			num_wste_characters += len(word) if word == wste_characters and ok_to_add else 0
			num_characters += len(word)
			ok_to_add = word != 'ἤ'

		return num_wste_characters / num_characters

	def freq_wste_precceded_by_eta(file):
		file = WordTokenizer('greek').tokenize(file)
		num_wste_characters = 0
		num_characters = 0
		wste_characters = 'ὥστε'
		ok_to_add = False

		for word in file:
			num_wste_characters += len(word) if word == wste_characters and ok_to_add else 0
			num_characters += len(word)
			ok_to_add = word == 'ἤ'

		return num_wste_characters / num_characters

	def freq_temporal_and_causal_clauses(file):
		file = WordTokenizer('greek').tokenize(file)
		num_clause_characters = 0
		num_characters = 0
		clause_chars = {'μέϰρι', 'ἕως', 'πρίν', 'πρὶν', 'ἐπεί', 'ἐπεὶ', 'ἐπειδή', 'ἐπειδὴ', 'ἐπειδάν', 'ἐπειδὰν', 'ὅτε', 'ὅταν'}
		clause_chars = clause_chars | \
		{normalize('NFD', val) for val in clause_chars} | \
		{normalize('NFC', val) for val in clause_chars} | \
		{normalize('NFKD', val) for val in clause_chars} | \
		{normalize('NFKC', val) for val in clause_chars}

		for word in file:
			num_clause_characters += len(word) if word in clause_chars else 0
			num_characters += len(word)

		return num_clause_characters / num_characters

	def variance_of_sentence_length(file):
		file = TokenizeSentence("greek").tokenize_sentences(file)
		num_sentences = 0
		total_len = 0

		for line in file:
			num_sentences += 1
			total_len += len(line)
		mean = total_len / num_sentences
		squared_difference = 0
		for line in file:
			squared_difference += (len(line) - mean) ** 2

		return squared_difference / num_sentences

	def particles_per_sentence(file):
		file = WordTokenizer('greek').tokenize(file)
		num_particles = 0
		particles = {'ἄν', 'ἂν', 'ἆρα', 'γε', "γ'", "δ'", 'δέ', 'δὲ','δή', 'δὴ', 'ἕως', "κ'", 'κε', 'κέ', 'κὲ', 'κέν', 'κὲν', \
		'κεν', 'μά', 'μὰ' 'μέν', 'μὲν', 'μέντοι', 'μή', 'μὴ', 'μήν', 'μὴν', 'μῶν', 'νύ', 'νὺ', 'νυ', 'οὐ', 'οὔ', 'οὒ', 'οὖν', \
		'περ', 'πω', "τ'", 'τε', 'τοι'}
		particles = particles | \
		{normalize('NFD', val) for val in particles} | \
		{normalize('NFC', val) for val in particles} | \
		{normalize('NFKD', val) for val in particles} | \
		{normalize('NFKC', val) for val in particles}

		for word in file:
			num_particles += 1 if word in particles else 0

		num_sentences = file.count('.') + file.count(';') + file.count(';') #Greek semi colon
		return num_particles / num_sentences

	def freq_raised_dot(file):
		#Unicode from https://en.wikipedia.org/wiki/Interpunct#Similar_symbols
		#'\u00B7' is '·', '\u0387' is '·', '\u2219' is '∙', '\u22C5' is '⋅', '\u2022' is '•', '\u16EB' is '᛫', '\u2027' is '‧', 
		#'\u2981' is '⦁', '\u2E33' is '⸳', '\u30FB' is '・', '\uA78F' is 'ꞏ', '\uFF65' is '･', '\U00010101' is '𐄁'
		dot_chars = {'·', '·', '∙', '⋅', '•', '᛫', '‧', '⦁', '⸳', '・', 'ꞏ', '･', '𐄁'}
		num_dot_chars = 0
		for char in file:
			num_dot_chars += 1 if char in dot_chars else 0
		return num_dot_chars / len(file)

	def freq_men(file):
		file = WordTokenizer('greek').tokenize(file)
		men_chars = {'μέν', 'μὲν'}
		men_chars = men_chars | \
		{normalize('NFD', val) for val in men_chars} | \
		{normalize('NFC', val) for val in men_chars} | \
		{normalize('NFKD', val) for val in men_chars} | \
		{normalize('NFKC', val) for val in men_chars}
		num_men = 0
		num_characters = 0
		for word in file:
			num_men += 1 if word in men_chars else 0
			num_characters += 1
		return num_men / num_characters


tesserae_clone_command = "git clone https://github.com/tesserae/tesserae.git"
greek_text_dir = "tesserae/texts/grc"

def main():
	global greek_text_dir

	#Associates files names to their respective features
	text_to_features = {}

	file_names = None
	if len(sys.argv) > 1 and sys.argv[1] == "testfile":
		file_names = {"tesserae/texts/grc/plato.respublica.tess"}

	#Download corpus if non-existent
	if not os.path.isdir(greek_text_dir):
		print("Corpus at " + greek_text_dir + " does not exist - attempting to clone repository...")
		os.system(tesserae_clone_command)

	#Obtain all the files to parse by traversing through the directory
	if file_names is None:
		file_names = {current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in \
		os.walk(greek_text_dir) for current_file_name in current_file_names if current_file_name.endswith(".tess")}

	"""
	Certain files in the tesserae corpus are not well formatted so they will be ommitted

	This file is very ill-formed
	tesserae/texts/grc/bacchylides.dithyrambs.tess

	The following dictionaries are a mapping from a character to the frequency they appear at the end of a sentence 
	(tokenized by the cltk sentence parser). Since we only want periods and semi colons, we will remove files with 
	large occurrences of characters that are not periods or semi colons. For example, polybius.histories.tess has 
	66 double quotes, 0 single quotes, and 62 right brackets at the end of its tokenized sentences.
	Since it has a large number of quotes and brackets, we will omit it.

	tesserae/texts/grc/polybius.histories.tess
		{": 66, ': 0, ]: 62}
	tesserae/texts/grc/apollonius.argonautica.tess
		{": 143, ': 0, ]: 2}
	tesserae/texts/grc/apollonius.argonautica/apollonius.argonautica.part.1.tess
		{": 28, ': 0, ]: 1}
	tesserae/texts/grc/apollonius.argonautica/apollonius.argonautica.part.3.tess
		{": 49, ': 0, ]: 0}
	tesserae/texts/grc/apollonius.argonautica/apollonius.argonautica.part.2.tess
		{": 31, ': 0, ]: 1}
	tesserae/texts/grc/apollonius.argonautica/apollonius.argonautica.part.4.tess
		{": 35, ': 0, ]: 0}
	tesserae/texts/grc/athenaeus.deipnosophists.tess
		{": 0, ': 183, ]: 0}
	tesserae/texts/grc/theophrastus.characters.tess
		{": 1, ': 20, ]: 0}
	"""
	file_names -= {'tesserae/texts/grc/bacchylides.dithyrambs.tess', \
	'tesserae/texts/grc/polybius.histories.tess', \
	'tesserae/texts/grc/apollonius.argonautica.tess', \
	'tesserae/texts/grc/apollonius.argonautica/apollonius.argonautica.part.1.tess', \
	'tesserae/texts/grc/apollonius.argonautica/apollonius.argonautica.part.3.tess', \
	'tesserae/texts/grc/apollonius.argonautica/apollonius.argonautica.part.2.tess', \
	'tesserae/texts/grc/apollonius.argonautica/apollonius.argonautica.part.4.tess', \
	'tesserae/texts/grc/athenaeus.deipnosophists.tess', \
	'tesserae/texts/grc/theophrastus.characters.tess'}

	#Feature extraction
	for file_name in file_names:
		text_to_features[file_name] = {}

		#Store each line of file in a list
		file_text = []
		with open(file_name, mode="r", encoding="utf-8") as file:
			for line in file:
				#Ignore lines without tess tags, or parse the tag out and strip whitespace
				if not line.startswith("<"):
					continue
				assert ">" in line
				line = line[line.index(">") + 1:].strip()
				file_text.append(line)

		#Convert list of strings into a single string
		file_text = " ".join(file_text)

		#Invoke the values of the Feature class which are functions
		#Default behavior is to invoke ALL functions of Features class. If names of features are specified on the 
		#command line, then only invoke those
		for feature in Features.__dict__.values() if len(sys.argv) == 1 else \
		[Features.__dict__[sys.argv[i]] for i in range(1, len(sys.argv)) if sys.argv[i] in Features.__dict__]:
			if callable(feature):
				score = feature(file_text)
				text_to_features[file_name][feature] = score
				print(file_name + ", " + str(feature) + ", " + str(score))

if __name__ == "__main__":
	main()
