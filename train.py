import pickle
import numpy as np
from sklearn import svm


def main():
	file_to_isprose = {}
	with open('classifications.csv', mode='r') as classification_file:
		classification_file.readline()
		for line in classification_file:
			line = line.strip().split(',')
			file_to_isprose[line[0]] = 1 if line[1] == 'True' else 0

	text_to_features = None
	with open('matrix.pickle', mode='rb') as pickle_file:
		text_to_features = pickle.loads(pickle_file.read())
	
	file_names = sorted([elem for elem in text_to_features.keys()])
	feature_names = sorted(list({feature for feature_to_val in text_to_features.values() for feature in feature_to_val.keys()}))
	data_1d = [text_to_features[file_name][feature] for file_name in file_names for feature in feature_names]
	data = []
	for i in range(len(file_names)):
		data.append([val for val in data_1d[i * len(feature_names): i * len(feature_names) + len(feature_names)]])
	target = [file_to_isprose[file_name] for file_name in file_names]

	assert data[-1][-1] == data_1d[-1]
	assert len(data) == len(target)
	assert len(feature_names) == len(data[0])

	data = np.asarray(data)
	target = np.asarray(target)

	classifier = svm.SVC(cache_size=200,class_weight=None,coef0=0.0,kernel='rbf',max_iter=-1,probability=False,random_state=None,\
	shrinking=True,tol=0.001,verbose=False)

if __name__ == '__main__':
	main()
