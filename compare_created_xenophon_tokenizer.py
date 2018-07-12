from cltk.utils.file_operations import open_pickle
from nltk.tokenize.punkt import PunktLanguageVars, PunktTrainer, PunktSentenceTokenizer
from extract_features import parse_tess

PunktLanguageVars.sent_end_chars = ('.', ';', ';')
PunktLanguageVars.internal_punctuation = (',', '·', ':')

text = parse_tess('tesserae/texts/grc/xenophon.anabasis.tess')
new_xeno_trainer = PunktTrainer()
# new_xeno_trainer.INCLUDE_ALL_COLLOCS = True
# new_xeno_trainer.INCLUDE_ABBREV_COLLOCS = True
new_xeno_trainer.train(text)
new_xeno_params = new_xeno_trainer.get_params()

tess_xeno_params = open_pickle('tokenizers/ancient_greek.pickle')._params

print(new_xeno_params.abbrev_types)
print(new_xeno_params.abbrev_types == tess_xeno_params.abbrev_types)
print()
print(new_xeno_params.collocations)
print(new_xeno_params.collocations == tess_xeno_params.collocations)
print()
print(new_xeno_params.sent_starters)
print(new_xeno_params.sent_starters == tess_xeno_params.sent_starters)
print()
print(new_xeno_params.ortho_context)
print(new_xeno_params.ortho_context == tess_xeno_params.ortho_context)
print()
