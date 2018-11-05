import pickle
import os
import re
from os.path import dirname, abspath, join
from collections import OrderedDict
from io import StringIO
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars

decorated_features = OrderedDict()

#The current python file must be in the same directory as tokenizers/
sentence_tokenizer_dir = join(dirname(abspath(__file__)), 'tokenizers')

#TODO It's a good idea to not make these None. Make blank objects and then mutate
word_tokenizer = None
sentence_tokenizers = None

def setup_tokenizers(terminal_punctuation):
	PunktLanguageVars.sent_end_chars = terminal_punctuation
	PunktLanguageVars.re_boundary_realignment = re.compile(r'[›»》’”\'\"）\)\]\}\>]+?(?:\s+|(?=--)|$)', re.MULTILINE)
	global word_tokenizer
	global sentence_tokenizers

	#Accessing private variables of PunktLanguageVars because nltk has a faulty design pattern that necessitates it.
	#Issue reported here: https://github.com/nltk/nltk/issues/2068
	word_tokenizer = PunktLanguageVars()
	word_tokenizer._re_word_tokenizer = re.compile(PunktLanguageVars._word_tokenize_fmt % {
	    'NonWord': r"(?:[\d\.\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡])",
	    'MultiChar': PunktLanguageVars._re_multi_char_punct,
	    'WordStart': r"[^\d\.\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡]",
	}, re.UNICODE | re.VERBOSE)
	word_tokenizer._re_period_context = re.compile(PunktLanguageVars._period_context_fmt % {
		'NonWord': r"(?:[\d\.\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡])",
		'SentEndChars': word_tokenizer._re_sent_end_chars, 
	}, re.UNICODE | re.VERBOSE)

	x = PunktLanguageVars()
	x._re_word_tokenizer = re.compile(PunktLanguageVars._word_tokenize_fmt % {
	    'NonWord': r"(?:[\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡])",
	    'MultiChar': PunktLanguageVars._re_multi_char_punct,
	    'WordStart': r"[^\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡]",
	}, re.UNICODE | re.VERBOSE)
	x._re_period_context = re.compile(PunktLanguageVars._period_context_fmt % {
		'NonWord': r"(?:[\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡])",
		'SentEndChars': x._re_sent_end_chars, 
	}, re.UNICODE | re.VERBOSE)

	#Read tokenizers from pickle files (also include an untrained tokenizer). Mapping from language name to tokenizer
	sentence_tokenizers = dict({None: PunktSentenceTokenizer(lang_vars=PunktLanguageVars())}, **{
		current_file_name[:current_file_name.index('.')]: pickle.load(open(join(current_path, current_file_name), mode='rb'))
		for current_path, current_dir_names, current_file_names in os.walk(sentence_tokenizer_dir) 
		for current_file_name in current_file_names if current_file_name.endswith('.pickle')
	})
	for s in sentence_tokenizers.values():
		s._lang_vars._re_period_context = x._re_period_context
		s._lang_vars._re_word_tokenizer = x._re_word_tokenizer

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
	'sentence_words': {
		'func': lambda lang, file: [word_tokenizer.word_tokenize(s) for s in sentence_tokenizers[lang].tokenize(file)], 
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
