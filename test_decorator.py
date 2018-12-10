from textual_feature import textual_feature, decorated_features, \
tokenize_types, clear_cache, debug_output, setup_tokenizers
import unittest

setup_tokenizers(('.', '?')) #'FULL STOP', 'SEMICOLON', 'GREEK QUESTION MARK'

@textual_feature('sentences', 'greek', debug=True)
def foo(file):
	return 'foo'

@textual_feature('sentences', 'greek', debug=True)
def bar(file):
	return 'bar'

@textual_feature('words', 'greek', debug=True)
def taz(file):
	return 'taz'

@textual_feature('words', 'greek', debug=True)
def qux(file):
	return 'qux'

@textual_feature('sentences', 'greek', debug=True)
def rup(file):
	return 'rup'

@textual_feature('sentences', 'greek', debug=True)
def lon(file):
	return 'lon'

@textual_feature('sentences', 'greek', debug=True)
def return_sentences(file):
	return file

@textual_feature('words', 'greek', debug=True)
def return_words(file):
	return file

class TestTextualFeature(unittest.TestCase):

	def setUp(self):
		clear_cache(tokenize_types, debug_output)

	def test_cache(self):
		file = 'test test. test test test test test test? test test. test.'

		filename = 'abc/def'
		foo(file, filename)
		bar(file, filename)
		rup(file, filename)
		self.assertEqual(debug_output.getvalue(), 'Cache hit! function: <bar>, filename: abc/def\n' + \
			'Cache hit! function: <rup>, filename: abc/def\n')

		clear_cache(tokenize_types, debug_output)

		filename = 'abc/ghi'
		foo(file, filename)
		taz(file, filename)
		qux(file, filename)
		self.assertEqual(debug_output.getvalue(), 'Cache hit! function: <qux>, filename: abc/ghi\n')
		filename = 'abc/jkl'
		foo(file, filename)
		bar(file, filename)
		taz(file, filename)
		qux(file, filename)
		self.assertEqual(debug_output.getvalue(), 'Cache hit! function: <qux>, filename: abc/ghi\n' + \
			'Cache hit! function: <bar>, filename: abc/jkl\n' + \
			'Cache hit! function: <qux>, filename: abc/jkl\n')

	def test_sentence_tokenization(self):
		file = 'test test. test test test test test test? test test. test.'
		filename = 'abc/def'
		self.assertEqual(return_sentences(file, filename), ['test test.', 'test test test test test test?', \
			'test test.', 'test.'])

	def test_word_tokenization(self):
		file = 'test test. test test test test test test? test test. test.'
		filename = 'abc/def'
		self.assertEqual(return_words(file, filename), ['test', 'test', '.', 'test', 'test', 'test', 'test', \
			'test', 'test', '?', 'test', 'test', '.', 'test', '.'])

	def test_loop_over_all_features(self):
		file = 'test test. test test test test test test? test test. test.'
		filename = 'abc/def'
		outputs = ['foo', 'bar', 'taz', 'qux', 'rup', 'lon', ['test test.', 'test test test test test test?', \
			'test test.', 'test.'], ['test', 'test', '.', 'test', 'test', 'test', 'test', 'test', 'test', '?', 'test', \
			'test', '.', 'test', '.']]

		i = 0
		for v in decorated_features.values():
			self.assertEqual(v(file, filename), outputs[i])
			i += 1

	def test_no_filename(self):
		file = 'test test. test test test test test test? test test. test.'
		filename = 'abc/def'
		self.assertEqual(foo(file, filename), foo(file))

if __name__ == '__main__':
	unittest.main()
