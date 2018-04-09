import pickle
from collections import OrderedDict

def main():
	prose_files = set()
	verse_files = set()
	with open('classifications.csv', mode='r') as classification_file:
		classification_file.readline()
		for line in classification_file:
			line = line.strip().split(',')
			if line[1] == 'True':
				prose_files.add(line[0])
			else:
				assert line[1] == 'False'
				verse_files.add(line[0])
	text_to_features = None
	with open('matrix.pickle', mode='rb') as pickle_file:
		text_to_features = pickle.loads(pickle_file.read())

if __name__ == '__main__':
	main()

