import os
import sys
from cltk.tokenize.sentence import TokenizeSentence

def feature_interrogative(file):
	num_interrogative = 0
	num_regular_sentence = 0

	for line in file:
		num_interrogative += line.count(";")
		num_regular_sentence += line.count(".")

	return num_interrogative / (num_interrogative + num_regular_sentence)

def feature_freq_conditional_characters(file):
	num_conditional_characters = 0
	num_characters = 0

	for line in file:
		num_conditional_characters += line.count("εἲ") + line.count("ἐάν") + line.count("εἰ")
		num_characters += len(line)

	return num_conditional_characters / num_characters

feature_list = [feature_interrogative, feature_freq_conditional_characters]

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

		#Convert list of strings into a single string, then break that into sentences using cltk tokenizer
		file_text = " ".join(file_text)
		tokenizer = TokenizeSentence("greek")
		file_text = tokenizer.tokenize_sentences(file_text)

		#Iterate over features
		for feature in feature_list:
			score = feature(file_text)
			text_to_features[file_name][feature] = score
			print(file_name + ", " + str(feature) + ", " + str(score))

if __name__ == "__main__":
	main()

"""
File "greek_feature.py", line 81, in <module>
    main()
  File "greek_feature.py", line 71, in main
    tokenizer = TokenizeSentence("greek")
  File "/Users/timgianitsos/Git/FeatureExtraction/env/lib/python3.6/site-packages/cltk/tokenize/sentence.py", line 35, in __init__
    self._setup_language_variables(self.language)
  File "/Users/timgianitsos/Git/FeatureExtraction/env/lib/python3.6/site-packages/cltk/tokenize/sentence.py", line 56, in _setup_language_variables
    'CLTK linguistics data not found for language {0}'.format(lang)
AssertionError: CLTK linguistics data not found for language greek

file = PUNCTUATION[lang]['file']
 11         rel_path = os.path.join('~/cltk_data',
 10                                 lang,
  9                                 'model/' + lang + '_models_cltk/tokenizers/sentence')  # pylint: disable=C0301
  8         path = os.path.expanduser(rel_path)
  7         tokenizer_path = os.path.join(path, file)
  6         assert os.path.isfile(tokenizer_path), \
  5             'CLTK linguistics data not found for language {0}'.format(lang)

"""