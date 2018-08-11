import pickle
import os
import re
from os.path import dirname, abspath, join
from collections import OrderedDict
from io import StringIO
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars

decorated_features = OrderedDict()

sentence_tokenizer_dir = join(dirname(abspath(__file__)), 'tokenizers')

#Read tokenizers from pickle files (also include an untrained tokenizer). Mapping from language name to tokenizer
sentence_tokenizers = dict({None: PunktSentenceTokenizer(lang_vars=PunktLanguageVars())}, **{
	current_file_name[:current_file_name.index('.')]: pickle.load(open(join(current_path, current_file_name), mode='rb'))
	for current_path, current_dir_names, current_file_names in os.walk(sentence_tokenizer_dir) 
	for current_file_name in current_file_names if current_file_name.endswith('.pickle')
})

#Accessing private variables of PunktLanguageVars because nltk has a faulty design pattern that necessitates it.
#Issue reported here: https://github.com/nltk/nltk/issues/2068
word_tokenizer = PunktLanguageVars()
word_tokenizer._re_word_tokenizer = re.compile(PunktLanguageVars._word_tokenize_fmt % {
    'NonWord': r"(?:[0-9\.?!\-)）\"“”‘’`··~,«»;;}\]\*\#:@&\'\(（{\[])",
    'MultiChar': PunktLanguageVars._re_multi_char_punct,
    'WordStart': r"[^0-9\.?!\-)）\"“”‘’`··~,«»;;}\]\*\#:@&\'\(（{\[]",
}, re.UNICODE | re.VERBOSE)

tokenize_types = {
	None: {
		'func': lambda lang, file: file, 
		'prev_filename': None, 
		'tokens': None, 
	}, 
	'sentences': {
		'func': lambda lang, file: sentence_tokenizers[lang].tokenize(file), 
		'prev_filename': None, 
		'tokens': None, 
	}, 
	'words': {
		'func': lambda lang, file: word_tokenizer.word_tokenize(file), 
		'prev_filename': None, 
		'tokens': None, 
	}, 
}

debug_output = StringIO()

def clear_cache(cache, debug):
	for k, v in cache.items():
		v['prev_filename'] = None
		v['tokens'] = None
	debug.truncate(0)
	debug.seek(0)

def textual_feature(tokenize_type=None, lang=None, debug=False):
	assert tokenize_type in tokenize_types, '"' + str(tokenize_type) + '" is not a valid tokenize type: Choose from among ' + \
		str(list(tokenize_types.keys()))
	assert lang in sentence_tokenizers, '"' + str(lang) + '" is not an available language: Choose from among ' + \
		str(list(sentence_tokenizers.keys()))
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
