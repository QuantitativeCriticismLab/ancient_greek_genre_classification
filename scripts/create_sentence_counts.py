from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars
from functools import reduce
import os
from os.path import join
from extract_features import _get_filenames, parse_tess
from greek_features import composite_files_to_exclude
from textual_feature import sentence_tokenizers

corpus_dir = join('tesserae', 'texts', 'grc')
files = _get_filenames(corpus_dir, 'tess', composite_files_to_exclude)

f = open('sentence_counts.csv', mode='w')
f.write('Data: https://github.com/timgianitsos/tesserae/tree/master/texts/grc,Project: https://www.qcrit.org,Author: Tim Gianitsos (tgianitsos@yahoo.com),Repo (Private): https://github.com/jdexter476/ProseVerseClassification.git,Commit: ' + os.popen('git rev-parse HEAD').read().strip() + '\n')
f.write('file name,number of sentences\n')
for file in files:
	file_text = parse_tess(file)
	num_sentences = len(sentence_tokenizers['ancient_greek'].tokenize(file_text))
	f.write(file[file.rindex(os.sep) + 1:] + ',' + str(num_sentences) + '\n')
print('Success!')
