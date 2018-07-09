#The greek.pickle used by cltk for ancient greek will unserialize as a PunktTrainer object.
#This script converts it into a PunktSentenceTokenizer

import os
import pickle
from cltk.utils.file_operations import open_pickle
from nltk.tokenize.punkt import PunktLanguageVars, PunktSentenceTokenizer

lang = 'greek'
file = 'greek.pickle'
PunktLanguageVars.sent_end_chars = ('.', ';', ';')
PunktLanguageVars.internal_punctuation = (',', '·', ':')
rel_path = os.path.join('~/cltk_data', lang, 'model/' + lang + '_models_cltk/tokenizers/sentence')
path = os.path.expanduser(rel_path)
tokenizer_path = os.path.join(path, file)

trainer = open_pickle(tokenizer_path)
trainer.INCLUDE_ALL_COLLOCS = True
trainer.INCLUDE_ABBREV_COLLOCS = True
tokenizer = PunktSentenceTokenizer(trainer.get_params())

with open('ancient_greek.pickle', 'wb') as pickle_file:
	pickle_file.write(pickle.dumps(tokenizer))
