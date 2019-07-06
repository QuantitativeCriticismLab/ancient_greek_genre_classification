import pickle
import os
import re
from inspect import signature
from os.path import dirname, abspath, join
from collections import OrderedDict
from io import StringIO
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars

decorated_features = OrderedDict()

#The current python file must be in the same directory as tokenizers/
sentence_tokenizer_dir = join(dirname(abspath(__file__)), 'tokenizers')

lang = None
word_tokenizer = None
sentence_tokenizers = None

tokenize_types = {
	None: {
		'func': lambda text: text, 
		'prev_filepath': None, 
		'tokens': None, 
	}, 
	'sentences': {
		'func': lambda text: sentence_tokenizers[lang].tokenize(text), 
		'prev_filepath': None, 
		'tokens': None, 
	}, 
	'words': {
		'func': lambda text: word_tokenizer.word_tokenize(text), 
		'prev_filepath': None, 
		'tokens': None, 
	}, 
	'sentence_words': {
		'func': lambda text: [word_tokenizer.word_tokenize(s) for s in sentence_tokenizers[lang].tokenize(text)], 
		'prev_filepath': None, 
		'tokens': None, 
	}, 
}

def setup_tokenizers(*, language=None, terminal_punctuation):
	global lang
	global word_tokenizer
	global sentence_tokenizers
	global tokenize_types
	lang = language
	PunktLanguageVars.sent_end_chars = terminal_punctuation
	PunktLanguageVars.re_boundary_realignment = re.compile(r'[›»》’”\'\"）\)\]\}\>]+?(?:\s+|(?=--)|$)', re.MULTILINE)
	for tokenize_type_data in tokenize_types.values():
		tokenize_type_data['prev_filepath'] = None
		tokenize_type_data['tokens'] = None

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

def reset_tokenizers():
	global word_tokenizer
	global sentence_tokenizers
	word_tokenizer = None
	sentence_tokenizers = None

debug_output = StringIO()

def clear_cache(cache, debug):
	for k, v in cache.items():
		v['prev_filepath'] = None
		v['tokens'] = None
	debug.truncate(0)
	debug.seek(0)

def textual_feature(*, tokenize_type=None, debug=False):
	global lang
	if not (word_tokenizer and sentence_tokenizers):
		raise ValueError('Tokenizers not initialized: Use "setup_tokenizers(terminal_punctuation=<collection of punctutation>)"')
	if tokenize_type not in tokenize_types:
		raise ValueError('"' + str(tokenize_type) + '" is not a valid tokenize type: Choose from among ' + 
			str(list(tokenize_types.keys())))
	if lang not in sentence_tokenizers:
		raise ValueError('"' + str(lang) + '" is not an available language: Choose from among ' + 
			str(list(sentence_tokenizers.keys())))
	def decor(f):
		#TODO make this more extensible. Use keyword args somehow instead of 'text' parameter?
		#TODO Ensure that features with duplicated names aren’t put in the ordered dict (this can happen if they come from different files)
		reqrd_params = {'text'}
		sig_params = signature(f).parameters
		if not all(tok in sig_params for tok in reqrd_params):
			raise ValueError('Error for "' + f.__name__ 
				+ '":\nMinimal required parameters: ' + str(reqrd_params) 
				+ '\nFound parameters: ' + str(set(sig_params)))
		def wrapper(*, text, filepath=None):
			if filepath:
				#TODO languages don't cache their own tokens, therefore using multiple languages will cause problems
				#Cache the tokenized version of this text if this filepath is new
				if tokenize_types[tokenize_type]['prev_filepath'] != filepath:
					tokenize_types[tokenize_type]['prev_filepath'] = filepath
					tokenize_types[tokenize_type]['tokens'] = tokenize_types[tokenize_type]['func'](text)
				elif debug:
					debug_output.write('Cache hit! ' + 'function: <' + f.__name__ + '>, filepath: ' + filepath + '\n')
				return f(tokenize_types[tokenize_type]['tokens'])
			else:
				return f(tokenize_types[tokenize_type]['func'](text))
		decorated_features[f.__name__] = wrapper
		return wrapper
	return decor
