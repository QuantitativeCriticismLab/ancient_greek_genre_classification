import pickle
from collections import OrderedDict

def main():
	author_to_isprose = OrderedDict()
	text_to_features = None
	with open('classifications.csv', mode='r') as classification_file:
		classification_file.readline()
		for line in classification_file:
			line = line.strip().split(',')
			author_to_isprose[line[0]] = line[1] == 'True'
	with open('matrix.pickle', mode='rb') as pickle_file:
		text_to_features = pickle.loads(pickle_file.read())

if __name__ == '__main__':
	main()

