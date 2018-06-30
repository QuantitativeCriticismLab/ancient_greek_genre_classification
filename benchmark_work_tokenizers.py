from nltk.tokenize.punkt import PunktLanguageVars
from cltk.tokenize.word import WordTokenizer
import re
import os
from timeit import timeit
from functools import partial
from extract_features import parse_tess, file_parsers
from progress_bar import print_progress_bar

p = PunktLanguageVars()
w = WordTokenizer('greek')

p._re_word_tokenizer = re.compile(PunktLanguageVars._word_tokenize_fmt % {
    'NonWord': r"(?:[?!.)\";;}\]\*:@\'\({\[])", #Incorporates period and greek question mark to exclude from word tokens (PunktLanguageVars._re_non_word_chars includes these in word tokens)
    'MultiChar': PunktLanguageVars._re_multi_char_punct,
    'WordStart': PunktLanguageVars._re_word_start,
}, re.UNICODE | re.VERBOSE)

corpus_dir = 'tesserae' + os.sep + 'texts' + os.sep + 'grc'
file_extension = 'tess'

file_names = sorted(list({current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in 
os.walk(corpus_dir) for current_file_name in current_file_names if current_file_name.endswith('.' + file_extension)}))

punkt_time = 0.0
trial_num = 1
for file_name in file_names:
	file_text = file_parsers[file_extension](file_name)
	punkt_time += timeit(partial(p.word_tokenize, file_text), number=1)
	print_progress_bar(trial_num, len(file_names), prefix='Progress')
	trial_num += 1

cltk_time = 0.0
trial_num = 1
for file_name in file_names:
	file_text = file_parsers[file_extension](file_name)
	cltk_time += timeit(partial(w.tokenize, file_text), number=1)
	print_progress_bar(trial_num, len(file_names), prefix='Progress')
	trial_num += 1

print('punkt_time: ' + str(punkt_time))
print('cltk_time: ' + str(cltk_time))




