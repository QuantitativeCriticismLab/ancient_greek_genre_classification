from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from unicodedata import normalize

features = []

tokenize_types = {\
	'sentences': {\
		'func': lambda lang, file: TokenizeSentence(lang).tokenize_sentences(file), \
		'prev_filename': None, \
		'tokens': None, \
	}, \
	'words': {\
		'func': lambda lang, file: WordTokenizer(lang).tokenize(file), \
		'prev_filename': None, \
		'tokens': None, \
	}
}

def textual_feature(tokenize_type, lang):
	def decor(f):
		def wrapper(file, filename):
			global tokenize_types
			if tokenize_types[tokenize_type]['prev_filename'] != filename:
				tokenize_types[tokenize_type]['prev_filename'] = filename
				tokenize_types[tokenize_type]['tokens'] = tokenize_types[tokenize_type]['func'](lang, file)
			else:
				print('Cache hit: ' + f.__name__ + ' ' + filename)
			return f(tokenize_types[tokenize_type]['tokens'])
		features.append(f.__name__)
		return wrapper
	return decor

@textual_feature('sentences', 'greek')
def freq_interrogatives(file):
	num_interrogative = 0

	for line in file:
		num_interrogative += line.count(';') + line.count(';')

	return num_interrogative / len(file)

@textual_feature('sentences', 'greek')
def bar(file):
	return 0

@textual_feature('sentences', 'greek')
def taz(file):
	return 0

@textual_feature('words', 'greek')
def freq_conditional_characters(file):
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

@textual_feature('sentences', 'greek')
def qux(file):
	return 0

@textual_feature('sentences', 'greek')
def lup(file):
	return 0

#Tests

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

print()

freq_conditional_characters(file, filename)
freq_conditional_characters(file, filename)

print()

print('Iteration:')
filename = 'abc/mno'
for f in features:
	print('\t' + f)
	globals()[f](file, filename)
