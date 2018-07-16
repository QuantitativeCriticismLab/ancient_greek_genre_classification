from color import *
import pickle
from extract_features import parse_tess
from progress_bar import print_progress_bar
from nltk.tokenize.punkt import *
import os

#Determine whether changing class variables in PunktLanguageVars affect pickle loads (it shouldn't)

before_params = pickle.load(open('tokenizers/english.pickle', mode='rb'))
before_params2 = PunktSentenceTokenizer()
before_params3 = PunktSentenceTokenizer('tesserae/texts/grc/xenophon.anabasis.tess')
PunktLanguageVars.sent_end_chars = ('%', '&', ';')
PunktLanguageVars.internal_punctuation = ('"', '1', '$')
after_params = pickle.load(open('tokenizers/english.pickle', mode='rb'))
after_params2 = PunktSentenceTokenizer()
after_params3 = PunktSentenceTokenizer('tesserae/texts/grc/xenophon.anabasis.tess')

file_names = sorted(list({current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in 
os.walk('tesserae/texts/grc') for current_file_name in current_file_names if current_file_name.endswith('.' + 'tess')}))

counter = 1
diff1 = 0
diff2 = 0
diff3 = 0
for file_name in file_names:
	file_text = parse_tess(file_name)
	diff1 += 1 if before_params.tokenize(file_text) != after_params.tokenize(file_text) else 0
	diff2 += 1 if before_params2.tokenize(file_text) != after_params2.tokenize(file_text) else 0
	diff3 += 1 if before_params3.tokenize(file_text) != after_params3.tokenize(file_text) else 0
	print_progress_bar(counter, len(file_names))
	counter += 1
print('Differences between pickle loads: ' + str(diff1))
print('Differences between default PunktSentenceTokenizers: ' + str(diff2))
print('Differences between trained PunktSentenceTokenizers: ' + str(diff3))
'''
Changing class variables in PunktLanguageVars seems to have no affect on any of the tokenizers before and after
'''

'''
Observe the following three snippets of code

(1)
>>> from nltk.tokenize.punkt import *
>>> s = 'test test test test test. test test test; test test.'
>>> PunktLanguageVars.sent_end_chars = ('.', ';')
>>> p = PunktSentenceTokenizer()
>>> p.tokenize(s)
['test test test test test.', 'test test test;', 'test test.']

(2)
>>> from nltk.tokenize.punkt import *
>>> s = 'test test test test test. test test test; test test.'
>>> p = PunktSentenceTokenizer()
>>> PunktLanguageVars.sent_end_chars = ('.', ';')
>>> p.tokenize(s)
['test test test test test.', 'test test test;', 'test test.']

(3)
>>> from nltk.tokenize.punkt import *; s = 'test test test test test. test test test; test test.'
>>> p = PunktSentenceTokenizer()
>>> p.tokenize(s)
['test test test test test.', 'test test test; test test.']
>>> PunktLanguageVars.sent_end_chars = ('.', ';')
>>> p.tokenize(s)
['test test test test test.', 'test test test; test test.']

The first two behave as one would expect, however (3) doesn't change it's tokenization, no matter what the 
PunktLanguageVars.sent_end_chars is set to. The difference is that the PunktLanguageVars.sent_end_chars is 
set AFTER tokenize() is called. This theoretically should make no difference, but after MUCH investigation, 
I discovered it was because of the way nltk initializes some variables on PunktLanguageVars objects. This 
is a bug that I will report to nltk's Github repo.

The _re_period_context instance variable is only set once in the method period_context_re(). Subsequent 
calls to period_context_re() yield the previous result.

def period_context_re(self):
    """Compiles and returns a regular expression to find contexts
    including possible sentence boundaries."""
    try:
        return self._re_period_context
    except:
        self._re_period_context = re.compile(
            self._period_context_fmt %
            {
                'NonWord': self._re_non_word_chars,
                'SentEndChars': self._re_sent_end_chars,
            },
            re.UNICODE | re.VERBOSE)
        return self._re_period_context

When I call p.tokenize(s), the period_context_re() method is invoked. Since _re_period_context has not been 
initialized, it will catch an exception and set it. However, now that _re_period_context is initialized, 
it will never be recomputed with the updated PunktLanguageVars.sent_end_chars.

To get around this, the _re_period_context variable will need to be set directly.

>>> from nltk.tokenize.punkt import *
>>> s = 'test test test test test. test test test; test test.'
>>> p = PunktSentenceTokenizer()
>>> p.tokenize(s)
['test test test test test.', 'test test test; test test.']
>>> 
>>> p._lang_vars._re_sent_end_chars
'[\\.\\?\\!]'
>>> PunktLanguageVars.sent_end_chars = ('.', ';')
>>> p.tokenize(s)
['test test test test test.', 'test test test; test test.']
>>> p._lang_vars._re_sent_end_chars
'[\\.\\;]'
>>> p._lang_vars._re_period_context
re.compile('\n        \\S*                          # some word material\n        [\\.\\?\\!]             # a potential sentence ending\n        (?=(?P<after_tok>\n            (?:[?!)\\";}\\]\\*:@\\\'\\({\\[])  , re.VERBOSE)
>>> 
>>> import re
>>> p._lang_vars._re_period_context = re.compile(p._lang_vars._period_context_fmt % {'NonWord': p._lang_vars._re_non_word_chars, 'SentEndChars': p._lang_vars._re_sent_end_chars,}, re.UNICODE | re.VERBOSE)
>>> p._lang_vars._re_period_context
re.compile('\n        \\S*                          # some word material\n        [\\.\\;]             # a potential sentence ending\n        (?=(?P<after_tok>\n            (?:[?!)\\";}\\]\\*:@\\\'\\({\\[])     , re.VERBOSE)
>>> PunktLanguageVars.sent_end_chars
('.', ';')
>>> p.tokenize(s)
['test test test test test.', 'test test test;', 'test test.']

'''
