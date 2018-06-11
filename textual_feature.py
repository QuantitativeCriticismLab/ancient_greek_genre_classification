from collections import OrderedDict
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from io import StringIO

decorated_features = OrderedDict()

tokenize_types = {\
	'default': {\
		'func': lambda lang, file: file, \
		'prev_filename': None, \
		'tokens': None, \
	}, \
	'sentences': {\
		'func': lambda lang, file: TokenizeSentence(lang).tokenize_sentences(file), \
		'prev_filename': None, \
		'tokens': None, \
	}, \
	'words': {\
		'func': lambda lang, file: WordTokenizer(lang).tokenize(file), \
		'prev_filename': None, \
		'tokens': None, \
	}, \
}

debug_output = StringIO()

def clear_cache(cache, debug):
	for k, v in cache.items():
		v['prev_filename'] = None
		v['tokens'] = None
	debug.truncate(0)
	debug.seek(0)

def textual_feature(tokenize_type, lang, debug=False):
	assert tokenize_type in tokenize_types, '"' + str(tokenize_type) + '" is not a valid tokenize type'
	def decor(f):
		def wrapper(file, filename=None):
			if filename:
				#Cache the tokenized version of this file if this filename is new
				if tokenize_types[tokenize_type]['prev_filename'] != filename:
					tokenize_types[tokenize_type]['prev_filename'] = filename
					tokenize_types[tokenize_type]['tokens'] = tokenize_types[tokenize_type]['func'](lang, file)
				elif debug:
					debug_output.write('Cache hit! ' + 'function: <' + f.__name__ + '>, filename: ' + filename + '\n')
				return f(tokenize_types[tokenize_type]['tokens'])
			else:
				return f(tokenize_types[tokenize_type]['func'](lang, file))
		decorated_features[f.__name__] = wrapper
		return wrapper
	return decor
