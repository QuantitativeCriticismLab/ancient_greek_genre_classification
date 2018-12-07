import os
from cltk.utils.file_operations import open_pickle
from extract_features import file_parsers
from progress_bar import print_progress_bar

xeno_tokenizer = open_pickle('tokenizers/ancient_greek.pickle')
tess_tokenizer = open_pickle('feature_data/tesserae_greek.pickle')
corpus_dir = 'tesserae' + os.sep + 'texts' + os.sep + 'grc'
file_extension = 'tess'
#Obtain all the files to parse by traversing through the directory
file_names = sorted(list({current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in \
os.walk(corpus_dir) for current_file_name in current_file_names if current_file_name.endswith('.' + file_extension)}))

counter = 1
for file_name in ['tesserae/texts/grc/achilles_tatius.leucippe_et_clitophon.tess']: #file_names:
	file_text = file_parsers[file_extension](file_name)
	x_tokens = xeno_tokenizer.tokenize(file_text)
	t_tokens = tess_tokenizer.tokenize(file_text)
	if t_tokens != x_tokens:
		xeno_out = open('feature_data/xeno_token_achilles.txt', mode='w')
		xeno_out.write('\n'.join(x_tokens))
		tess_out = open('feature_data/tess_token_achilles.txt', mode='w')
		tess_out.write('\n'.join(t_tokens))
	# print_progress_bar(counter, len(file_names))
	counter += 1

'''
I trained Punkt on the entire tesserae corpus (feature_data/tesserae_greek.pickle). It's performance was actually worse than the tokenizer that was created from training on just Xenophon (tokenizers/ancient_greek.pickle). The tokenizer created from training on just Xenophon does well, except for failing to tokenize sentences where the terminal punctuation is not followed by a space.
'''
