import unittest
from greek_features import *
from functools import reduce

class TestGreekFeatures(unittest.TestCase):

	def setUp(self):
		pass

	def test_freq_indefinite_pronoun_in_non_interrogative_sentence1(self):
		file = 'test test. test test test? test test test; test test. test.'
		result = freq_indefinite_pronoun_in_non_interrogative_sentence(file)
		expected = 0
		self.assertEqual(expected, result)

	def test_freq_indefinite_pronoun_in_non_interrogative_sentence2(self):
		file = 'τις τινός τινός, αβγ δεζ. ηθικλ τις μνξοπρσ; τινός. τω τι τυφχψω.'
		result = freq_indefinite_pronoun_in_non_interrogative_sentence(file)
		expected = 21 / 39
		self.assertEqual(expected, result)

	def test_freq_vocative_sentences1(self):
		file = 'ὦ α βγδ ὦ εζθικλ. μνξ ὦ οπ, ρσὦ τυ; φχψω. ὦ.'
		result = freq_vocative_sentences(file)
		expected = 3 / 4
		self.assertEqual(expected, result)

	def test_non_interoggative_sentence_with_relative_clause1(self):
		file = 'ὅς αφνιοςε ςοεφπκ. ὃ ςενςεο; ΝΕΣΟΝΦΕΙΝΟΣΙ ὧν. ὧν. νψςειοιοςνφψλε.'
		result = non_interoggative_sentence_with_relative_clause(file)
		expected = 3 / 4
		self.assertEqual(expected, result)

	def test_mean_sentence_length1(self):
		file = 'ὅς αφνιοςε ςοεφπκ. ὃ ςενςεο; ΝΕΣΟΝΦΕΙΝΟΣΙ ὧν. ὧν. νψςειοιοςνφψλε.'
		result = mean_sentence_length(file)
		expected = (16 + 8 + 15 + 3 + 15) / 5
		self.assertEqual(expected, result)

	def test_variance_of_sentence_length1(self):
		file = 'ὅς αφνιοςε ςοεφπκ. ὃ ςενςεο; ΝΕΣΟΝΦΕΙΝΟΣΙ ὧν. ὧν. νψςειοιοςνφψλε.'
		result = variance_of_sentence_length(file)
		vals = (16, 8, 15, 3, 15)
		mean = sum(vals) / len(vals)
		expected = reduce(lambda cur_sum, val: cur_sum + (val - mean) ** 2, vals, 0) / len(vals)
		self.assertEqual(expected, result)

	def test_relative_clause_per_sentence1(self):
		file = 'ὅς αφνιοςε ςοεφπκ. ὃ ςενςεο; ΝΕΣΟΝΦΕΙΝΟΣΙ ὧν αἷς. ὧν. νψςειοιοςνφψλε. ἥ ἥ ἥ ἥ ἥ.'
		result = relative_clause_per_sentence(file)
		expected = 9 / 5
		self.assertEqual(expected, result)

	def test_freq_interrogatives1(self):
		file = 'a b ccccccc. aaafew aaedwp bbdinwe; bnoirenfiob; ads ofiihwio; freino. daieof; frinoe.'
		#TODO GREEK question doesn't work 'a b ccccccc. aaafew aaedwp bbdinwe; bnoirenfiob; ads ofiihwio; freino. daieof; frinoe.'
		result = freq_interrogatives(file)
		expected = 4 / 7
		self.assertEqual(expected, result)

if __name__ == '__main__':
	unittest.main()
