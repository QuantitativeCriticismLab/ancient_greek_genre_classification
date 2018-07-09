import sys
import os
import pickle
from nltk.tokenize.punkt import PunktLanguageVars, PunktTrainer, PunktSentenceTokenizer
from cltk.tokenize.sentence import TokenizeSentence
from extract_features import file_parsers
from progress_bar import print_progress_bar

# This doesn't work
# class CustomLanguageVars(PunktLanguageVars):
# 	sent_end_chars = ('.', ';', ';')
# 	internal_punctuation = (',', '·', ':')
# trainer = PunktTrainer(train_text='test test test. test test test test. test test; test test.', lang_vars=CustomLanguageVars())
# trainer.INCLUDE_ALL_COLLOCS = True
# trainer.INCLUDE_ABBREV_COLLOCS = True
# params = trainer.get_params()
# tkzr = PunktSentenceTokenizer(params)
# s = 'test test test. test test test test test; test test. test test'
# print(tkzr.tokenize(s))

lang = sys.argv[1] if len(sys.argv) >= 2 else input('Enter language: ')

PunktLanguageVars.sent_end_chars = ('.', ';', ';')
PunktLanguageVars.internal_punctuation = (',', '·', ':')
trainer = PunktTrainer(lang_vars=PunktLanguageVars())
trainer.INCLUDE_ALL_COLLOCS = True
trainer.INCLUDE_ABBREV_COLLOCS = True

corpus_dir = 'tesserae' + os.sep + 'texts' + os.sep + 'grc'
file_extension = 'tess'
#Obtain all the files to parse by traversing through the directory
file_names = sorted(list({current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in \
os.walk(corpus_dir) for current_file_name in current_file_names if current_file_name.endswith('.' + file_extension)}))

counter = 1
for file_name in file_names:
	file_text = file_parsers[file_extension](file_name)
	trainer.train(file_text, verbose=False, finalize=False)
	print_progress_bar(counter, len(file_names))
	counter += 1

with open(lang + '.pickle', 'wb') as pickle_file:
	pickle_file.write(pickle.dumps(PunktSentenceTokenizer(trainer.get_params())))

# params = trainer.get_params()
# tkzr = PunktSentenceTokenizer(params)
# # s = 'test test test test test. test test test test. test test. test test; test test test.'
# s = 'test test test. test test test test test; test test. test test'
# print(tkzr.tokenize(s))
# print(TokenizeSentence('greek').tokenize_sentences(s))
