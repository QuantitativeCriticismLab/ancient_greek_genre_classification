from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer

decorated_features = []

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

#TODO think about if decorator parameter is None?
def textual_feature(tokenize_type, lang, debug=False):
	def decor(f):
		def wrapper(file, filename):
			if tokenize_types[tokenize_type]['prev_filename'] != filename:
				tokenize_types[tokenize_type]['prev_filename'] = filename
				tokenize_types[tokenize_type]['tokens'] = tokenize_types[tokenize_type]['func'](lang, file)
			elif debug:
				print('*** Cache hit! ' + 'function: <' + f.__name__ + '>, filename: ' + filename + ' ***')
			return f(tokenize_types[tokenize_type]['tokens'])
		decorated_features.append((wrapper, f.__name__))
		return wrapper
	return decor
