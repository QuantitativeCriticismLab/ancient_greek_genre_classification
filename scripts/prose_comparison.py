names_from_author_labels = set()
names_from_prose_list = set()

f = open('author_labels.txt')
for line in f:
	line = line.strip()
	if line.endswith('p'):
		names_from_author_labels.add(line.split(' - ')[0].replace(' ', '_').lower())
f = open('tesserae/texts/prose_list')
for line in f:
	if line == '# greek\n':
		break
for line in f:
	line = line.replace('\\', '').replace('.', '').replace('\n', '')
	names_from_prose_list.add(line)
print(names_from_author_labels)
print(names_from_prose_list)
print()
print(names_from_author_labels - names_from_prose_list)
print(names_from_prose_list - names_from_author_labels)

'''
Currently investigating how Punkt sentence tokenizers are trained. The default nltk greek sentence tokenizer seems to have been trained from Modern Greek.

File                Language            Source                             Contents                Size of training corpus(in tokens)           Model contributed by
=======================================================================================================================================================================
greek.pickle        Greek               Efstathios Stamatatos              To Vima (TO BHMA)               ~227,000                             Jan Strunk / Tibor Kiss

It seems that "To Vima" is a newspaper.


The cltk greek.pickle file is a PunktTrainer object, whereas the nltk greek.pickle files are PunktSentenceTokenizer objects.

>>> f = open('/Users/timgianitsos/cltk_data/greek/model/greek_models_cltk/tokenizers/sentence/greek.pickle', mode='rb'); type(pickle.loads(f.read()))
<class 'nltk.tokenize.punkt.PunktTrainer'>
>>> f = open('/Users/timgianitsos/nltk_data/tokenizers/punkt/greek.pickle', mode='rb'); type(pickle.loads(f.read()))
<class 'nltk.tokenize.punkt.PunktSentenceTokenizer'>
>>> f = open('/Users/timgianitsos/nltk_data/tokenizers/punkt/PY3/greek.pickle', mode='rb'); type(pickle.loads(f.read()))
<class 'nltk.tokenize.punkt.PunktSentenceTokenizer'>

What is greek.pickle from CLTK from? It is "comprised of the entirety of the Xenophon's Anabasis"
https://github.com/cltk/greek_training_set_sentence_cltk

There are two greek.pickle files that were downloaded from NLTK. One is ~/nltk_data/tokenizers/punkt/greek.pickle, and the other is ~/nltk_data/tokenizers/punkt/PY3/greek.pickle. I'm assuming the former is for Python 2, and the latter is for Python 3. The former is serialized as text whereas the latter is serialized as binary.

'''

'''

I realized that the tesserae repo had a file called prose_list which included all the prose classifications - I didn't need to ask Joseph for them after all. So I have two points of reference for classifications: the author_labels.txt based on the data that Joseph gave me, and prose_list in the tesserae repo. I compared them to make sure they were congruent.

The classifications are almost identical except the tesserae file doesn't include these four authors as prose: {'eusebius_caeserea', 'philostratus', 'plutarch_amatorius', 'tryphiodorus'}

The first three {'eusebius_caeserea', 'philostratus', 'plutarch_amatorius'} are not an issue.

In the case of 'eusebius_caeserea', it is the result of a simple mispelling. In my classifications I include "Eusebius Caesarea" and "Eusebius Caeserea" because there are files with either spelling in the tesserae repo.

In the case of 'philostratus', the prose_list file has 'philostratus_the_athenian' and 'philostratus_the_lemnian', just not 'philostratus' by itself. These should all be prose anyway.

In the case of 'plutarch_amatorius', that is a mistake in the naming schema for one of the files in the tesserae repo, and I had to include it to make everything consistent. There should only be 'plutarch' because 'plutarch_amatorius' is not a person - 'amatorius' is the name of one of plutarch's works, so the tesserae people just made a mistake when naming the file. I filed an issue about it on Github.
https://github.com/tesserae/tesserae/issues/57

However in the case of 'tryphiodorus' it seems as though Joseph labeled it prose, but when I look online it says it is poetry. Curiously however, it was never misclassified by the RandomForest classifier. Perhaps it is a strange edge case of poetry that is more similar to prose.

'''
