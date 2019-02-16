#latin_prose.csv: Counter({'history': 91, 'oratory': 64, 'letters': 64, 'philosophy': 55, 'technical treatise': 43, 'miscellaneous': 40})
#latin_verse.csv: Counter({'epic': 115, 'miscellaneous': 50, 'drama': 36, 'elegy': 29})

from collections import OrderedDict
import pickle

categories = {'prose': 'latin/latin_prose.csv', 'verse': 'latin/latin_verse.csv'}
for prosody, filename in categories.items():
	labels_filename = 'latin/labels/' + prosody + '_labels.csv'
	feature_data_filename = 'feature_data/latin_' + prosody + '.pickle'
	with open(filename, mode='r') as latin_file:
		feature_names = latin_file.readline().strip().split(',')[2:]
		text_name_to_features = {}
		genre_name_to_genre_val = OrderedDict()
		text_name_to_genre_val = OrderedDict()
		for line in latin_file:
			line = line.strip().split(',')
			text_name, genre_name, feature_vals = line[0], line[1].lower().replace(' ', '_'), line[2:]
			assert len(feature_names) == len(feature_vals)
			text_name_to_features[text_name] = {feature_name: feature_val for feature_name, feature_val in zip(feature_names, feature_vals)}
			if genre_name not in genre_name_to_genre_val:
				genre_name_to_genre_val[genre_name] = len(genre_name_to_genre_val)
			text_name_to_genre_val[text_name] = genre_name_to_genre_val[genre_name]
		with open(labels_filename, mode='w') as genre_file:
			genre_file.write(','.join(k + ':' + str(v) for k, v in genre_name_to_genre_val.items()) + '\n')
			genre_file.write('Textname,Genre\n')
			for text_name, genre_val in text_name_to_genre_val.items():
				genre_file.write(text_name + ',' + str(genre_val) + '\n')
		print('Successfully created ' + prosody + ' label file ' + labels_filename)
		with open(feature_data_filename, mode='wb') as pickle_file:
			pickle_file.write(pickle.dumps(text_name_to_features))
		print('Successfully created ' + prosody + ' feature data file ' + feature_data_filename)
