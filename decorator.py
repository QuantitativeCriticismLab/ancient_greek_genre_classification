from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer

last_tokenized_sentence_filename = None
sentence_tokens = None #cached tokenized file

def tokenize_sentences(lang):
	def decor(f):
		def wrapper(file, filename):
			global sentence_tokens
			global last_tokenized_sentence_filename
			if not last_tokenized_sentence_filename or last_tokenized_sentence_filename != filename:
				tokenizer = TokenizeSentence(lang)
				last_tokenized_sentence_filename = filename
				sentence_tokens = tokenizer.tokenize_sentences(file)
			return f(sentence_tokens)
		return wrapper
	return decor

@tokenize_sentences('greek')
def freq_interrogatives(file):
	num_interrogative = 0

	for line in file:
		num_interrogative += line.count(';') + line.count(';')

	return num_interrogative / len(file)

@tokenize_sentences('greek')
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

# file = 'a' * 100

# freq_interrogatives(file)
# freq_interrogatives(file)
# bar(file)
# freq_interrogatives(file)
# bar(file)
# bar(file)

# print()

# file = 'a' * 99
# bar(file)
# freq_interrogatives(file)

# print()

# file = 'a' * 101
# freq_interrogatives(file)
# bar(file)

#Tests 2

file = 'a' * 100
filename = 'abc/def'

freq_interrogatives(file, filename)
freq_interrogatives(file, filename)
bar(file, filename)
freq_interrogatives(file, filename)
bar(file, filename)
bar(file, filename)

print()

filename = 'abc/ghi'
bar(file, filename)
freq_interrogatives(file, filename)

print()

filename = 'abc/jkl'
file = 'a' * 101
freq_interrogatives(file, filename)
bar(file, filename)

