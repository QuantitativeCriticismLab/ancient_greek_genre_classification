from ml_analyzers import *
from analyze_models import main

main('notes/751_all_features.pickle', 'labels/prosody_labels.csv', None)
main('notes/751_all_features.pickle', 'labels/genre_labels.csv', None)
main('notes/610_prose_features.pickle', 'labels/genre_labels.csv', None)
main('notes/141_verse_features.pickle', 'labels/genre_labels.csv', None)
