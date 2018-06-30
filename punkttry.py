from nltk.tokenize.punkt import PunktLanguageVars
from cltk.tokenize.word import WordTokenizer
import re

p = PunktLanguageVars()
w = WordTokenizer('greek')

p._re_word_tokenizer = re.compile(PunktLanguageVars._word_tokenize_fmt % {
    'NonWord': r"(?:[?!.)\";;}\]\*:@\'\({\[])", #Incorporates period and greek question mark to exclude from word tokens (PunktLanguageVars._re_non_word_chars includes these in word tokens)
    'MultiChar': PunktLanguageVars._re_multi_char_punct,
    'WordStart': PunktLanguageVars._re_word_start,
}, re.UNICODE | re.VERBOSE)


s = 'test test test. test test; test test? test test test test test. test. test test. test? test test.'
assert p.word_tokenize(s) == w.tokenize(s)

d = [('tesserae/texts/grc/achilles_tatius.leucippe_et_clitophon.tess', 'notes/a.txt', 'notes/b.txt'), 
	('tesserae/texts/grc/bacchylides.epinicians.tess', 'notes/m.txt', 'notes/n.txt'), 
	('tesserae/texts/grc/polybius.histories.tess', 'notes/x.txt', 'notes/y.txt')]

for t in d:
	with open(t[0], mode='r', encoding='utf-8') as f:
		from io import StringIO
		file_text = StringIO()
		for line in f:
			#Ignore lines without tess tags, or parse the tag out and strip whitespace
			if not line.startswith('<'):
				continue
			assert '>' in line
			file_text.write(line[line.index('>') + 1:].strip())
			file_text.write(' ')
		s = file_text.getvalue()
		punk_out = open(t[1], mode='w')
		punk_out.write('\n\n'.join(p.word_tokenize(s)))
		cltk_out = open(t[2], mode='w')
		cltk_out.write('\n\n'.join(w.tokenize(s)))
		# assert p.word_tokenize(s) == w.tokenize(s)

# with open('tesserae/texts/grc/achilles_tatius.leucippe_et_clitophon.tess') as f:
# 	s = f.read()
# 	punk_out = open('a.txt', mode='w')
# 	punk_out.write('\n\n'.join(p.word_tokenize(s)))
# 	cltk_out = open('b.txt', mode='w')
# 	cltk_out.write('\n\n'.join(w.tokenize(s)))
# 	# assert p.word_tokenize(s) == w.tokenize(s)



