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

old_tok_out = open('feature_data/old_tok.txt', mode='w')
old_tok_out.write('\n'.join(tokenizer.tokenize(text)))
new_tok_out = open('feature_data/new_tok.txt', mode='w')
new_tok_out.write('\n'.join(new_tokenizer.tokenize(text)))


'''
There seem to be very few abbreviations in the tesserae corpus. This means training the PunktSentenceTokenizer might not yield any improvement.
From paper abstract: "[Punkt sentence tokenization training] is based on the assumption that a large number of ambiguities in the determination of sentence boundaries can be eliminated once abbreviations have been identified."


The Punkt sentence tokenizer doesn't do a good job of tokenizing sentences when there is no space between the terminating period, and the first word of the next sentence. These occurrences are typos in the tesserae corpus however - there should always be spaces between terminal punctuation and the first word of the next sentence.

This regex had 18463 matches across 238 files
It looks for a period outside of a tess tag that is followed by a greek letter
(?!\..*?>)\.[α-ωΑ-Ω]

This regex had 350047 matches across 816 files
It looks for all periods outside of a tess tag
(?!\..*?>)\.

Periods followed by a word with no whitespace in-between account for 18463 / 350047 = 5.27% percent of all terminal periods.

'''
