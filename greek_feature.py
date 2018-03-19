import os
import sys
import math
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from cltk.stem.lemma import LemmaReplacer

class Features:
	def freq_interrogatives(file):
		file = TokenizeSentence("greek").tokenize_sentences(file)
		num_interrogative = 0

		for line in file:
			num_interrogative += line.count(";")

		return num_interrogative / len(file)

	def freq_conditional_characters(file):
		file = WordTokenizer('greek').tokenize(file)
		num_conditional_characters = 0
		num_characters = 0

		for word in file:
			num_conditional_characters += len(word) if word == "εἲ" or word == "ἐάν" or word == "εἰ" else 0#Accent should be acute?
			num_characters += len(word)

		return num_conditional_characters / num_characters

	def freq_personal_pronouns(file):
		file = LemmaReplacer('greek').lemmatize(file)
		num_pronouns = 0
		num_characters = 0

		for word in file:
			num_pronouns += len(word) if word == "ἐγώ" or word == "ἐμέω" or word == "σύ" or word == "σεύω" else 0
			num_characters += len(word)

		return num_pronouns / num_characters

	def freq_demonstrative(file):
		file = LemmaReplacer('greek').lemmatize(file)
		num_demonstratives = 0
		num_characters = 0

		for word in file:
			num_demonstratives += len(word) if word == 'ἐκεῖνος' or word == 'αὕται' or word == 'οὗτος' or word == 'τόδε' \
			or word == 'τάδε' or word == 'ἐκείνᾱς' or word == 'τάσσω' or word == 'ταύτᾱς' or word == 'ὅδε' else 0
			num_characters += len(word)

		return num_demonstratives / num_characters

	def freq_indefinite_pronoun_in_non_interrogative_sentence(file):
		# Extremely time consuming
		# file = TokenizeSentence("greek").tokenize_sentences(file)
		# num_pronouns = 0
		# num_characters = 0
		# for line in file:
			# line = LemmaReplacer('greek').lemmatize(line)
			# if ';' not in line:
			# 	for word in line:
			# 		num_pronouns += len(word) if word == 'τις' else 0
			# 		num_characters += len(word)

		#TODO Need to check for interrogatives
		file = LemmaReplacer('greek').lemmatize(file)
		num_pronouns = 0
		num_characters = 0

		for word in file:
			num_pronouns += len(word) if word == 'τις' else 0
			num_characters += len(word)

		return num_pronouns / num_characters

	def freq_allos(file):
		file = LemmaReplacer('greek').lemmatize(file)
		num_allos = 0
		num_characters = 0

		for word in file:
			num_allos += len(word) if word == 'ἄλλος' or word == 'ἄλλᾱς' else 0
			num_characters += len(word)

		return num_allos / num_characters

	def freq_autos(file):
		file = LemmaReplacer('greek').lemmatize(file)
		num_autos = 0
		num_characters = 0

		for word in file:
			num_autos += len(word) if word == 'αὐτός' or word == 'αὐτᾱς' else 0
			num_characters += len(word)

		return num_autos / num_characters

	def freq_reflexive(file):
		file = LemmaReplacer('greek').lemmatize(file)
		num_reflexive = 0
		num_characters = 0

		for word in file:
			num_reflexive += len(word) if word == 'ἐμαυτοῦ' or word == 'σαυτοῦ' or word == 'ἑαυτοῦ' else 0
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
		return 0

	def mean_length_relative_clause(file):
		return 0

	#Count of relative pronouns in non-interrogative sentences / total non-interrogative sentences
	def relative_clause_per_sentence(file):
		file = TokenizeSentence("greek").tokenize_sentences(file)
		num_relative_pronoun = 0
		num_non_interrogative_sentence = 0
		pronouns = {'ὅς', 'οὗ', 'ᾧ', 'ὅν', 'οἵ', 'ὧν', 'οἷς', 'οὕς', 'ἥ', 'ᾗς', 'ἥν', 'αἵ', 'αἷς', 'ἅς', 'ὅ', 'ἅ'}

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
		clause_characters = {'μέϰρι', 'ἕως', 'πρίν', 'πρὶν', 'ἐπεί', 'ἐπειδή', 'ἐπειδὴ', 'ἐπειδάν', 'ἐπειδὰν', 'ὅτε', 'ὅταν'}

		for word in file:
			num_clause_characters += len(word) if word in clause_characters else 0
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


tesserae_clone_command = "git clone https://github.com/tesserae/tesserae.git"
greek_text_dir = "tesserae/texts/grc"

def main():
	global greek_text_dir

	#Associates files names to their respective features
	text_to_features = {}

	file_names = None
	if len(sys.argv) > 1:
		if sys.argv[1] == "debug": #if debug, just scan pre-selected corpus
			file_names = ["tesserae/texts/grc/polybius.histories.tess"]
		else: #Allows user to select custom path other than tesserae
			greek_text_dir = sys.argv[1]

	#Download corpus if non-existent
	if not os.path.isdir(greek_text_dir):
		print("Corpus at " + greek_text_dir + " does not exist - attempting to clone repository...")
		os.system(tesserae_clone_command)

	#Obtain all the files to parse by traversing through the directory
	if file_names is None:
		file_names = [current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in \
		os.walk(greek_text_dir) for current_file_name in current_file_names if current_file_name.endswith(".tess")]

	#Feature extraction
	for file_name in file_names:
		text_to_features[file_name] = {}

		#Store each line of file in a list
		file_text = []
		with open(file_name, "r") as file:
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
		for feature in Features.__dict__.values():
			if callable(feature):
				score = feature(file_text)
				text_to_features[file_name][feature] = score
				print(file_name + ", " + str(feature) + ", " + str(score))

if __name__ == "__main__":
	main()
