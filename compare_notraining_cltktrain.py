import os
from cltk.utils.file_operations import open_pickle
from nltk.tokenize.punkt import PunktLanguageVars, PunktTrainer, PunktSentenceTokenizer
from progress_bar import print_progress_bar
from extract_features import file_parsers

PunktLanguageVars.sent_end_chars = ('.', ';', ';')
PunktLanguageVars.internal_punctuation = (',', '·', ':')

notrain_tokenizer = PunktSentenceTokenizer()
cltk_tokenizer = open_pickle('tokenizers/ancient_greek.pickle')
kjohnson_tokenizer = PunktSentenceTokenizer(open_pickle('notes/kjohnson_greek.pickle').get_params())

corpus_dir = 'tesserae' + os.sep + 'texts' + os.sep + 'grc'
file_extension = 'tess'

#Obtain all the files to parse by traversing through the directory
file_names = sorted(list({current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in \
os.walk(corpus_dir) for current_file_name in current_file_names if current_file_name.endswith('.' + file_extension)}))

counter = 1
f = open('notes/diff_tokenizers_notrain_cltk.txt', mode='w')
f.write('Differences:\n\n')
for file_name in file_names:
	file_text = file_parsers[file_extension](file_name)
	n_tokens = notrain_tokenizer.tokenize(file_text)
	c_tokens = cltk_tokenizer.tokenize(file_text)
	k_tokens = kjohnson_tokenizer.tokenize(file_text)
	if n_tokens != c_tokens:
		f.write(file_name + ' 1')
	if n_tokens != k_tokens:
		f.write(file_name + ' 2')
	if c_tokens != k_tokens:
		f.write(file_name + ' 3')
	print_progress_bar(counter, len(file_names))
	counter += 1
