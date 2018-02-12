import os
import sys

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
		num_conditional_characters += line.count("εἲ") + line.count("ἐάν")
		num_characters += len(line)

	return num_conditional_characters / num_characters

feature_list = [feature_interrogative, feature_freq_conditional_characters]

tesserae_clone_command = "git clone https://github.com/tesserae/tesserae.git"
greek_text_dir = "tesserae/texts/grc"

def main():

	#Download corpus if non-existent
	if not os.path.isdir(greek_text_dir):
		print("Corpus does not exist - attempting to clone repository...")
		os.system(tesserae_clone_command)

	#Obtain files to parse
	text_to_features = {}
	file_names = []
	for current_path, current_dir_names, current_file_names in os.walk(greek_text_dir):
		for current_file_name in current_file_names:
			f = str(current_path + os.sep + current_file_name)
			file_names.append(f)
			text_to_features[f] = {}

	#Feature extraction
	for file_name in file_names:
		file_text = []
		with open(file_name, "r") as file:
			for line in file:
				#Ignore lines without tess tags, or parse the tag out and strip whitespace
				if not line.startswith("<"):
					continue
				assert ">" in line
				line = line[line.index(">") + 1:].strip()
				file_text.append(line)

		for feature in feature_list:
			score = feature(file_text)
			text_to_features[file_name][feature] = score
			print(file_name + ", " + str(feature) + ", " + str(score))

if __name__ == "__main__":
	main()
