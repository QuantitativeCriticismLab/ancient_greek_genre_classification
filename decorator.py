from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer

sentence_tokens = None #cached tokenized file

def tokenize_sentences(f):
	tokenizer = TokenizeSentence('greek') #TODO other languages
	def tokenized_input_sen(file):
		eq = True
		global sentence_tokens

		#Check if the cached tokenized file is equal to the provided file
		if sentence_tokens is None:
			eq = False
		else:
			i = 0
			while i < len(file) and eq:
				for tok in sentence_tokens:
					if tok != file[i: len(tok)]:
						eq = False
						break
					i += len(tok)


		if not eq:
			sentence_tokens = tokenizer.tokenize_sentences(file)
		else:
			print('Cache hit: ' + str(f))
		return f(sentence_tokens)
	return tokenized_input_sen

@tokenize_sentences
def freq_interrogatives(file):
	num_interrogative = 0

	for line in file:
		num_interrogative += line.count(';') + line.count(';')

	return num_interrogative / len(file)

@tokenize_sentences
def bar(file):
	return 0


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

#Tests

file = 'a' * 100

freq_interrogatives(file)
freq_interrogatives(file)
bar(file)
freq_interrogatives(file)
bar(file)
bar(file)

print()

file = 'a' * 99
bar(file)
freq_interrogatives(file)

print()

file = 'a' * 101
freq_interrogatives(file)
bar(file)