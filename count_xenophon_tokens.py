from extract_features import parse_tess
from cltk.utils.file_operations import open_pickle
from nltk.tokenize.punkt import PunktLanguageVars, PunktTrainer, PunktSentenceTokenizer

PunktLanguageVars.sent_end_chars = ('.', ';', ';')
PunktLanguageVars.internal_punctuation = (',', '·', ':')

text = parse_tess('tesserae/texts/grc/xenophon.anabasis.tess')
tokenizer = open_pickle('tokenizers/ancient_greek.pickle')
print('Xenophon tokens: ' + str(len(tokenizer.tokenize(text))))
print()

trainer = PunktTrainer(lang_vars=PunktLanguageVars())
trainer.INCLUDE_ALL_COLLOCS = True
trainer.INCLUDE_ABBREV_COLLOCS = True
trainer.train(text, verbose=True)

new_tokenizer = PunktSentenceTokenizer(trainer.get_params())
print('tokenizers equal? ' + str(tokenizer == new_tokenizer))
print('tokenization equal? ' + str(tokenizer.tokenize(text) == new_tokenizer.tokenize(text)))

old_tok_out = open('notes/old_tok.txt', mode='w')
old_tok_out.write('\n'.join(tokenizer.tokenize(text)))
new_tok_out = open('notes/new_tok.txt', mode='w')
new_tok_out.write('\n'.join(new_tokenizer.tokenize(text)))
