def main():
	text_to_features = {}
	with open("tesserae/texts/grc/achilles_tatius.leucippe_et_clitophon.tess", "r") as file:
		num_interrogative = 0
		num_regular_sentence = 0
		for line in file:
			line = line[line.index('>') + 1:] #parse out .tess tags
			num_interrogative += line.count(';')
			num_regular_sentence += line.count('.')
		print("Fraction of Interrogatives: " + str(num_interrogative / (num_interrogative + num_regular_sentence)))

if __name__ == "__main__":
	main()
