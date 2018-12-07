import os
from cltk.utils.file_operations import open_pickle
from nltk.tokenize.punkt import PunktLanguageVars, PunktTrainer, PunktSentenceTokenizer
from progress_bar import print_progress_bar
from extract_features import file_parsers

PunktLanguageVars.sent_end_chars = ('.', ';', ';')
PunktLanguageVars.internal_punctuation = (',', '·', ':')

cltk_params = open_pickle('tokenizers/ancient_greek.pickle')._params
kjohnson_params = open_pickle('feature_data/kjohnson_greek.pickle').get_params()

#Are the attributes from ~/cltk_data/greek/model/greek_models_cltk/tokenizers/sentence/greek.pickle the same as https://github.com/cltk/greek_training_set_sentence_cltk/blob/master/greek.pickle ? Yes they are
print(cltk_params.abbrev_types)
print(cltk_params.abbrev_types == kjohnson_params.abbrev_types)
print()
print(cltk_params.collocations)
print(cltk_params.collocations == kjohnson_params.collocations)
print()
print(cltk_params.sent_starters)
print(cltk_params.sent_starters == kjohnson_params.sent_starters)
print()
print(cltk_params.ortho_context)
print(cltk_params.ortho_context == kjohnson_params.ortho_context)
print()
p = PunktSentenceTokenizer()._params
print('Defaults')
print(p.abbrev_types)
print(p.collocations)
print(p.sent_starters)
print(p.ortho_context)



