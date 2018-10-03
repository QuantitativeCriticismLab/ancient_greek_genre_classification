from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars
from functools import reduce
import os
from os.path import join
from extract_features import _get_filenames, parse_tess
from greek_features import composite_files_to_exclude
from textual_feature import sentence_tokenizers

corpus_dir = join('tesserae', 'texts', 'grc')
files = _get_filenames(corpus_dir, 'tess', composite_files_to_exclude)

f = open('character_counts_with_spaces.csv', mode='w')
f.write('Data: https://github.com/timgianitsos/tesserae/tree/master/texts/grc,Project: https://www.qcrit.org,Author: Tim Gianitsos (tgianitsos@yahoo.com),Repo (Private): https://github.com/jdexter476/ProseVerseClassification.git,Commit: ' + os.popen('git rev-parse HEAD').read().strip() + '\n')
f.write('file name,character count (spaces ARE included between words but not between sentences, and punctuation is included)\n')
for file in files:
	file_text = parse_tess(file)
	char_count = reduce(lambda count_so_far, sentence: count_so_far + len(sentence), sentence_tokenizers['ancient_greek'].tokenize(file_text), 0)
	f.write(file[file.rindex(os.sep) + 1:] + ',' + str(char_count) + '\n')
print('Success!')
