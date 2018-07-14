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

'''
I got the internal PunktParameters object from the cltk pickle file that was trained on Xenophon's Anabasis (https://github.com/cltk/greek_training_set_sentence_cltk/blob/master/training_sentences.txt), and I also got the internal PunktParameters object from an PunktTrainer that I created from training on Xenophon's Anabasis from the tesserae corpus (https://github.com/tesserae/tesserae/blob/master/texts/grc/xenophon.anabasis.tess).

The values of the instance variables were as follows:
abbrev_types
    cltk: {'ὄν', 'ἐᾶν', 'ἔζη'}
    tess: set()

collocations
    cltk: set()
    tess: set()

sent_starters
    cltk: {'οἱ', 'ταύτην', 'ἀκούσαντες', 'μετὰ', 'οὐκοῦν', 'καίτοι', 'ἐπεὶ', 'ἀλλὰ', 'εἰ', 'καὶ', 'ἀκούσας', 'ὁ', 'ἐκ', 'ἔνθα', 'ταῦτα', 'τοιγαροῦν', 'ἐπειδὴ', 'ἐνταῦθα', 'ἐντεῦθεν'}
    tess: set()

ortho_context
    cltk: Too long to display
    tess: Too long to display (differs from cltk's)




NLTK suggests setting these variables on a PunktTrainer before using it.
new_xeno_trainer.INCLUDE_ALL_COLLOCS = True
new_xeno_trainer.INCLUDE_ABBREV_COLLOCS = True

I wanted to test whether setting these variables made a difference for the PunktTrainer being trained on tesserae's xenophon.anabasis.tess at https://github.com/tesserae/tesserae/blob/master/texts/grc/xenophon.anabasis.tess. I checked the fours instance variables on my PunktParameters created with and without setting INCLUDE_ALL_COLLOCS and INCLUDE_ABBREV_COLLOCS.
The only difference was the collocations variable. Without setting INCLUDE_ALL_COLLOCS and INCLUDE_ABBREV_COLLOCS, it is the empty set(). When I do set these variables to True, it becomes {('δεδήλωται', 'ἐκ'), ('πολλά', 'ταῦτα'), ('στάδια', 'ἐπεὶ'), ('ποιεῖν', 'ἐπεὶ'), ('δεδήλωται', 'ἐπεὶ'), ('τάδε', 'ἄνδρες'), ('ἐπεσιτίσαντο', 'ἐντεῦθεν'), ('̓ασίαν', 'ὁ'), ('ἐπίστευεν', 'ἐπεὶ'), ('ἐσώθη', 'καὶ'), ('χωρίον', 'ἐνταῦθα'), ('χεῖρα', 'ἀνέτειναν'), ('οἰκουμένην', 'ἐνταῦθα'), ('τοιάδε', 'ἐγώ'), ('ποταμόν', 'ἐνταῦθα'), ('χώρᾳ', 'ἐνταῦθα'), ('τοιάδε', 'ἄνδρες'), ('εἵποντο', 'ἐπεὶ'), ('οἰκουμένην', 'ἐνταῦθ'), ('ἐκπλεῖν', 'ὁ'), ('τάδε', 'ἐγώ'), ('εὐδαίμονα', 'ἐνταῦθα'), ('ἀρχήν', 'ὁ')}.
'''