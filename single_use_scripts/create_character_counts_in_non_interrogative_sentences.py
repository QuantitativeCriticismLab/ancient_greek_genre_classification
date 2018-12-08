from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars
from functools import reduce
import os
from os.path import join
from extract_features import _get_filenames, parse_tess
from greek_features import composite_files_to_exclude
import textual_feature

corpus_dir = join('tesserae', 'texts', 'grc')
files = _get_filenames(corpus_dir, 'tess', composite_files_to_exclude)

f = open('character_counts_in_non_interrogative_sentences.csv', mode='w')
f.write('Data: https://github.com/timgianitsos/tesserae/tree/master/texts/grc,Project: https://www.qcrit.org,Author: Tim Gianitsos (tgianitsos@yahoo.com),Repo (Private): https://github.com/jdexter476/ProseVerseClassification.git,Code commit: ' + os.popen('git rev-parse HEAD').read().strip() + ',Corpus commit: ' + os.popen('git -C "./tesserae" rev-parse HEAD').read().strip() + '\n')
f.write('file name,character count (spaces not included and punctuation is included)\n')
textual_feature.setup_tokenizers(('.', ';', ';'))
for file in files:
	file_text = parse_tess(file)
	char_count = sum(len(word) 
		for sentence in 
			(textual_feature.word_tokenizer.word_tokenize(line) 
			for line in textual_feature.sentence_tokenizers['ancient_greek'].tokenize(file_text) 
			if line[-1] not in {';', ';'} and len(line) > 1 and line[-2] not in {';', ';'})
		for word in sentence)
	f.write(file[file.rindex(os.sep) + 1:] + ',' + str(char_count) + '\n')
print('Success!')
