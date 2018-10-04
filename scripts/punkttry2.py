from textual_feature import sentence_tokenizers
from nltk.tokenize.punkt import PunktLanguageVars, PunktSentenceTokenizer
import re

p = PunktLanguageVars()

p._re_word_tokenizer = re.compile(PunktLanguageVars._word_tokenize_fmt % {
    'NonWord': r"(?:[0-9\.?!\-)）\"“”‘’`··~,«»;;}\]\*\#:@&\'\(（{\[])",
    'MultiChar': PunktLanguageVars._re_multi_char_punct,
    'WordStart': r"[^0-9\.?!\-)）\"“”‘’`··~,«»;;}\]\*\#:@&\'\(（{\[]",
}, re.UNICODE | re.VERBOSE)

s = 'Σιδὼν ἐπὶ θαλάττῃ πόλις, ̓Ασσυρίων ἡ θάλασσα. test ""test test? test test. test test! test test. test. test test; test: test; test; test23 test45 89test. test test” test test “test test“. "test test". test test... test‘ test’. 00000test. test.test. .....test. test-test test- test. test） test test（ test test. «test test» test.'
print(p.word_tokenize(s))
print()

s = '"ss ss". "ss ss." «s s. abc 123409 abc. 5ff5g s. ~ab cd~ ab~cd s.'
print(p.word_tokenize(s))
print()

# From polybius.histories.tess
s = '1συμμάχοις. ἀποδοῦναι Καρχηδονίους ̔Ρωμαίοις "1χωρὶς λύτρων ἅπαντας τοὺς αἰχμαλώτους. ἀργυ"1ρίου κατενεγκεῖν Καρχηδονίους ̔Ρωμαίοις ἐν ἔτεσιν "1εἴκοσι δισχίλια καὶ διακόσια τάλαντα Εὐβοϊκά."2'
print(p.word_tokenize(s))
print()

# From polybius.histories.tess
s = "διόπερ οὐχ ὁρῶν ποίαν ἄν τις ὀξυτέραν ἢ μείζονα λάβοι μεταβολὴν τῶν καθ' ἡμᾶς τῆς γε ̔Ρωμαίοις συμβάσης, εἰς τοῦτον ἀπεθέμην τὸν καιρὸν τὸν ὑπὲρ τῶν προειρημένων ἀπολογισμόν: γνοίη δ' ἄν τις τὸ μέγεθος τῆς μεταβολῆς ἐκ τούτων. ζήτει ἐν τῷ περὶ στρατηγίας. [εχξ. Vατ. π. 369 μαι. 24, 4 ηεψς.]"
print(p.word_tokenize(s))
print()



#Sentence Tokenization

s = 'a b c. "a b c". a b c. "a b c." a b c. “a b c”. a b c. “a b c.” a b c.'
print('\n'.join(PunktSentenceTokenizer(lang_vars=PunktLanguageVars()).tokenize(s)))
print()

s = 'a b c. "a b c". a b c. "a b c." a b c. “a b c”. a b c. “a b c.” a b c.'
PunktLanguageVars.re_boundary_realignment = re.compile(r'["”\')\]}]+?(?:\s+|(?=--)|$)', re.MULTILINE)
p = PunktLanguageVars()
p._re_word_tokenizer = re.compile(PunktLanguageVars._word_tokenize_fmt % {
    'NonWord': r"(?:[0-9\-)）\"“”‘’`··~,«»;;}\]\*\#:@&\'\(（{\[])",
    'MultiChar': PunktLanguageVars._re_multi_char_punct,
    'WordStart': r"[^0-9\-)）\"“”‘’`··~,«»;;}\]\*\#:@&\'\(（{\[]",
}, re.UNICODE | re.VERBOSE)
p._re_period_context = re.compile(PunktLanguageVars._period_context_fmt % {
    'NonWord': r"(?:[0-9\-)）\"“”‘’`··~,«»;;}\]\*\#:@&\'\(（{\[])",
    'SentEndChars': PunktLanguageVars._re_sent_end_chars,
},
re.UNICODE | re.VERBOSE)
tok = PunktSentenceTokenizer(lang_vars=p)
print('\n'.join(tok.tokenize(s)))
print()
