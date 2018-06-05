from textual_feature import textual_feature, decorated_features, tokenize_types

@textual_feature('sentences', 'greek', debug=True)
def foo(file):
	return 'I am foo\n' + str(file) + '\n\n'

@textual_feature('sentences', 'greek', debug=True)
def bar(file):
	return 'I am bar\n' + str(file) + '\n\n'

@textual_feature('words', 'greek', debug=True)
def taz(file):
	return 'I am taz\n' + str(file) + '\n\n'

@textual_feature('words', 'greek', debug=True)
def qux(file):
	return 'I am qux\n' + str(file) + '\n\n'

@textual_feature('sentences', 'greek', debug=True)
def rup(file):
	return 'I am rup\n' + str(file) + '\n\n'

@textual_feature('sentences', 'greek', debug=True)
def lon(file):
	return 'I am lon\n' + str(file) + '\n\n'

file = 'test test. test test test test test test; test test. test.'
filename = 'abc/def'

for t in decorated_features:
	print(t[0](file, filename))

# from unicodedata import normalize
# @textual_feature('sentences', 'greek')
# def freq_interrogatives(file):
# 	num_interrogative = 0

# 	for line in file:
# 		num_interrogative += line.count(';') + line.count(';')

# 	return num_interrogative / len(file)

# @textual_feature('sentences', 'greek')
# def bar(file):
# 	return 0

# @textual_feature('sentences', 'greek')
# def taz(file):
# 	return 0

# @textual_feature('words', 'greek')
# def freq_conditional_characters(file):
# 	num_conditional_characters = 0
# 	num_characters = 0

# 	conditional_characters = {'εἰ', 'εἴ', 'εἲ', 'ἐάν', 'ἐὰν'}
# 	conditional_characters = conditional_characters | \
# 	{normalize('NFD', val) for val in conditional_characters} | \
# 	{normalize('NFC', val) for val in conditional_characters} | \
# 	{normalize('NFKD', val) for val in conditional_characters} | \
# 	{normalize('NFKC', val) for val in conditional_characters}

# 	for word in file:
# 		num_conditional_characters += len(word) if word in conditional_characters else 0
# 		num_characters += len(word)

# 	return num_conditional_characters / num_characters

# @textual_feature('sentences', 'greek')
# def qux(file):
# 	return 0

# @textual_feature('sentences', 'greek')
# def lup(file):
# 	return 0

# #Tests

# file = 'a' * 100
# filename = 'abc/def'

# freq_interrogatives(file, filename)
# freq_interrogatives(file, filename)
# bar(file, filename)
# freq_interrogatives(file, filename)
# bar(file, filename)
# bar(file, filename)

# print()

# filename = 'abc/ghi'
# bar(file, filename)
# freq_interrogatives(file, filename)

# print()

# filename = 'abc/jkl'
# file = 'a' * 101
# freq_interrogatives(file, filename)
# bar(file, filename)

# print()

# freq_conditional_characters(file, filename)
# freq_conditional_characters(file, filename)

# print()

# print('Iteration:')
# filename = 'abc/mno'
# for f in features:
# 	print('\t' + f)
# 	globals()[f](file, filename)
