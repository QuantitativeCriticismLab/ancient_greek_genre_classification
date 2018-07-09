from nltk.tokenize.punkt import PunktLanguageVars, PunktTrainer, PunktSentenceTokenizer
from cltk.tokenize.sentence import TokenizeSentence

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


PunktLanguageVars.sent_end_chars = ('.', ';', ';')
PunktLanguageVars.internal_punctuation = (',', '·', ':')
trainer = PunktTrainer(train_text='test test test. test test test test. test test; test test.', lang_vars=PunktLanguageVars())
trainer.INCLUDE_ALL_COLLOCS = True
trainer.INCLUDE_ABBREV_COLLOCS = True
params = trainer.get_params()
tkzr = PunktSentenceTokenizer(params)
# s = 'test test test test test. test test test test. test test. test test; test test test.'
s = 'test test test. test test test test test; test test. test test'
print(tkzr.tokenize(s))
print(TokenizeSentence('greek').tokenize_sentences(s))
