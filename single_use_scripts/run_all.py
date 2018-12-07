from ml_analyzers import *
from analyze_models import main

main('feature_data/751_all_features.pickle', 'labels/prosody_labels.csv', None)
main('feature_data/751_all_features.pickle', 'labels/genre_labels.csv', None)
main('feature_data/610_prose_features.pickle', 'labels/genre_labels.csv', None)
main('feature_data/141_verse_features.pickle', 'labels/genre_labels.csv', None)

prose_labels = ['prose_miscellaneous', 'letters', 'technical_treatise', 'oratory', 'history', 'philosophy']
verse_labels = ['drama', 'epic', 'verse_miscellaneous']

for l in prose_labels:
	main('feature_data/610_prose_features.pickle', 'labels/' + l + '_vs_rest_of_prose.csv', None)

for l in verse_labels:
	main('feature_data/141_verse_features.pickle', 'labels/' + l + '_vs_rest_of_verse.csv', None)
