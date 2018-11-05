import re
import sys
import os
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars
from extract_features import parse_tess

PunktLanguageVars.sent_end_chars = ('.', ';', ';')
PunktLanguageVars.re_boundary_realignment = re.compile(r'[›»》’”\'\"）\)\]\}\>]+?(?:\s+|(?=--)|$)', re.MULTILINE)

new_reg = PunktLanguageVars()
new_reg._re_word_tokenizer = re.compile(PunktLanguageVars._word_tokenize_fmt % {
    'NonWord': r"(?:[\d\.\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡])",
    'MultiChar': PunktLanguageVars._re_multi_char_punct,
    'WordStart': r"[^\d\.\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡]",
}, re.UNICODE | re.VERBOSE)
new_reg._re_period_context = re.compile(PunktLanguageVars._period_context_fmt % {
	'NonWord': r"(?:[\d\.\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡])",
	'SentEndChars': new_reg._re_sent_end_chars, 
}, re.UNICODE | re.VERBOSE)
new_reg_t = PunktSentenceTokenizer(lang_vars=new_reg)

new_reg_no_per = PunktLanguageVars()
new_reg_no_per._re_word_tokenizer = re.compile(PunktLanguageVars._word_tokenize_fmt % {
    'NonWord': r"(?:[\d\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡])",
    'MultiChar': PunktLanguageVars._re_multi_char_punct,
    'WordStart': r"[^\d\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡]",
}, re.UNICODE | re.VERBOSE)
new_reg_no_per._re_period_context = re.compile(PunktLanguageVars._period_context_fmt % {
	'NonWord': r"(?:[\d\?¿؟\!¡！‽…⋯᠁ฯ,،，､、。°※··᛫~\:;;\\\/⧸⁄（）\(\)\[\]\{\}\<\>\'\"‘’“”‹›«»《》\|‖\=\-\‐\‒\–\—\―_\+\*\^\$£€§%#@&†‡])",
	'SentEndChars': new_reg_no_per._re_sent_end_chars, 
}, re.UNICODE | re.VERBOSE)
new_reg_no_per_t = PunktSentenceTokenizer(lang_vars=new_reg_no_per)

old_t = PunktSentenceTokenizer()


# skip = [] #Insert files to skip here
# for current_path, current_dir_names, current_file_names in os.walk('tesserae/texts/grc', topdown=True):
# 	for current_file_name in current_file_names:
# 		if current_path + os.sep + current_file_name in skip:
# 			print('Skipping ' + current_path + os.sep + current_file_name + '...')
# 			continue
# 		print('Reading ' + current_path + os.sep + current_file_name + '...')
# 		s = parse_tess(current_path + os.sep + current_file_name)
# 		reg_sentences = new_reg_t.tokenize(s)
# 		no_period_sentences = new_reg_no_per_t.tokenize(s)
# 		if reg_sentences != no_period_sentences:
# 			print(reg_sentences)
# 			print('\n\n\n\n\n\n\n\n\n')
# 			print(no_period_sentences)
# 			sys.exit()

skip = ['tesserae/texts/grc/plutarch.de_fortuna.tess'] #Insert files to skip here
for current_path, current_dir_names, current_file_names in os.walk('tesserae/texts/grc', topdown=True):
	for current_file_name in current_file_names:
		if current_path + os.sep + current_file_name in skip:
			print('Skipping ' + current_path + os.sep + current_file_name + '...')
			continue
		print('Reading ' + current_path + os.sep + current_file_name + '...')
		s = parse_tess(current_path + os.sep + current_file_name)
		old_sentences = old_t.tokenize(s)
		no_period_sentences = new_reg_no_per_t.tokenize(s)
		if old_sentences != no_period_sentences:
			print(old_sentences)
			print('\n\n\n\n\n\n\n\n\n')
			print(no_period_sentences)
			sys.exit()
