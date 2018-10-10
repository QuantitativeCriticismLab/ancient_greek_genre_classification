import unittest
from nltk.tokenize.punkt import PunktLanguageVars
from textual_feature import tokenize_types

PunktLanguageVars.sent_end_chars = ('.', ';', ';') #'FULL STOP', 'SEMICOLON', 'GREEK QUESTION MARK'

class TestParsers(unittest.TestCase):

	def setUp(self):
		pass

	def test_sentences1(self):
		file = 'test test. test test test? test test test; test test. test.'
		result = tokenize_types['sentences']['func']('ancient_greek', file)
		expected = ['test test.', 'test test test? test test test;', 'test test.', 'test.']
		self.assertEqual(expected, result)

	def test_sentence_words1(self):
		file = 'test test. test test test? test test test; test test. test.'
		result = tokenize_types['sentence_words']['func']('ancient_greek', file)
		expected = [['test', 'test', '.'], ['test', 'test', 'test', '?', 'test', 'test', 'test', ';'], 
		['test', 'test', '.'], ['test', '.']]
		self.assertEqual(expected, result)

	def test_sentence_words2(self):
		file = 'a b ccccccc. aaa aa bb; bb; ads ofiihwio; freino. daieof; frinoe.'
		result = tokenize_types['sentence_words']['func']('ancient_greek', file)
		expected = [['a', 'b', 'ccccccc', '.'], ['aaa', 'aa', 'bb', ';'], ['bb', ';'], ['ads', 'ofiihwio', ';'], 
		['freino', '.'], ['daieof', ';'], ['frinoe', '.']]
		self.assertEqual(expected, result)

if __name__ == '__main__':
	unittest.main()
