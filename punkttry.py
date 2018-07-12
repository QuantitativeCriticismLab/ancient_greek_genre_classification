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



'''
cltk is not extensible for any language. Word tokenization is limited to certain languages in the constructor even though the tokenize() method isn't restrictive. Even in word.py, they notice this. They write "Necessary? since we have an 'else' in `tokenize`"

def __init__(self, language):
        """Take language as argument to the class. Check availability and
        setup class variables."""
        self.language = language
        self.available_languages = ['arabic', 
                                    'french',
                                    'greek',
                                    'latin',
                                    'old_norse']
        assert self.language in self.available_languages, \
            "Specific tokenizer not available for '{0}'. Only available for: '{1}'.".format(self.language,  # pylint: disable=line-too-long
            self.available_languages)  # pylint: disable=line-too-long
        # ^^^ Necessary? since we have an 'else' in `tokenize`


The ancient greek in cltk hasn't even been fully implemented yet. From the doc string: "This is a placeholder function that returns the default NLTK word tokenizer until Greek-specific options are added"

def tokenize_greek_words(text):
    """
    Tokenizer divides the string into a list of substrings. This is a placeholder
    function that returns the default NLTK word tokenizer until
    Greek-specific options are added.
    
    Example:
    >>> text = 'Θουκυδίδης Ἀθηναῖος ξυνέγραψε τὸν πόλεμον τῶν Πελοποννησίων καὶ Ἀθηναίων,'
    >>> tokenize_greek_words(text)
    ['Θουκυδίδης', 'Ἀθηναῖος', 'ξυνέγραψε', 'τὸν', 'πόλεμον', 'τῶν', 'Πελοποννησίων', 'καὶ', 'Ἀθηναίων', ',']
      
    :param string: This accepts the string value that needs to be tokenized
    :returns: A list of substrings extracted from the string
    """
    
    return nltk_tokenize_words(text) # Simplest implementation to start


Sentence tokenization seems to be its own area of research in unsupervised learning
https://dl.acm.org/citation.cfm?id=1245122

Punkt word tokenizer w/ modified regex is superior to cltk word tokenizer in that it removes periods from words even when they are followed by quotes
'''
