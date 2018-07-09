#https://stackoverflow.com/questions/33139531/preserve-empty-lines-with-nltks-punkt-tokenizer
from nltk.tokenize.punkt import PunktLanguageVars, PunktSentenceTokenizer

class CustomLanguageVars(PunktLanguageVars):
	_period_context_fmt = r"""
		\S*                          # some word material
		%(SentEndChars)s             # a potential sentence ending
		(?=(?P<after_tok>
			%(NonWord)s              # either other punctuation
			|
			\s*(?P<next_tok>\S+)     # or 0 or more whitespace and some other token
		))"""

custom_tknzr = PunktSentenceTokenizer(lang_vars=CustomLanguageVars())

s = "test test test test.test test test test\n test test test. test?\n\n test test test test?\n\n\n"

print(custom_tknzr.tokenize(s))
