import os

tesserae_clone_command = "git clone https://github.com/tesserae/tesserae.git"
greek_text_dir = "tesserae/texts/grc"

def main():
	if not os.path.isdir(greek_text_dir):
		os.system(tesserae_clone_command)

	text_to_features = {}
	file_names = []
	for current_path, current_dir_names, current_file_names in os.walk(greek_text_dir):
		file_names += [current_path + os.sep + current_file_name for current_file_name in current_file_names]

	for file_name in file_names:
		print("Reading " + file_name)
		with open(file_name, "r") as file:
			num_interrogative = 0
			num_regular_sentence = 0
			for line in file:

				#Ignore lines without tess tags, or parse the tag out and strip whitespace
				if not line.startswith('<'):
					continue
				line = line[line.index('>') + 1:].strip()

				num_interrogative += line.count(';')
				num_regular_sentence += line.count('.')

			print("	Fraction of Interrogatives: " + str(num_interrogative / (num_interrogative + num_regular_sentence)))

if __name__ == "__main__":
	main()
