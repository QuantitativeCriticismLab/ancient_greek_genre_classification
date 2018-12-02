from collections import Counter, OrderedDict
from extract_features import _get_filenames
import os
cnt = Counter()
labels = OrderedDict()

prose_genre_file = open('prose_genre.csv')
prose_genre_file.readline()
prose_genre_file.readline()
prose_genre_file.readline()
pg = OrderedDict()
for line in prose_genre_file:
	line = line.strip().split(',')
	line[1] = line[1].replace(' ', '_')
	if line[1] == 'miscellaneous':
		line[1] = 'prose_miscellaneous'
	if line[1] not in labels:
		labels[line[1]] = len(labels)
	pg[line[0]] = line[1]
cnt.update(pg.values())
assert len(pg) == 610
assert pg['achilles_tatius.leucippe_et_clitophon.tess'] == 'prose_miscellaneous'
assert pg['xenophon.anabasis.tess'] == 'history'
assert sum(cnt.values()) == len(pg)
print('Prose genres:', set(pg.values()))

verse_genre_file = open('verse_genre.csv')
verse_genre_file.readline()
verse_genre_file.readline()
verse_genre_file.readline()
vg = OrderedDict()
for line in verse_genre_file:
	line = line.strip().split(',')
	line[1] = line[1].replace(' ', '_')
	if line[1] == 'miscellaneous':
		line[1] = 'verse_miscellaneous'
	if line[1] not in labels:
		labels[line[1]] = len(labels)
	vg[line[0]] = line[1]
cnt.update(vg.values())
assert len(vg) == 141
assert vg['aeschylus.agamemnon.tess'] == 'drama'
assert vg['tryphiodorus.the_taking_of_ilios.tess'] == 'epic'
assert sum(cnt.values()) == len(pg) + len(vg)
print('Verse genres:', set(vg.values()))
print('Counts:', cnt)

print('Category key:', labels)

filename_to_path = {s[s.rindex(os.sep) + 1:]: s for s in _get_filenames('tesserae/texts/grc', 'tess', set())}
path_to_filename = {s: s[s.rindex(os.sep) + 1:] for s in _get_filenames('tesserae/texts/grc', 'tess', set())}
assert len(filename_to_path) == len(path_to_filename)
file_to_genre = dict(**pg, **vg)
output_file = 'genre_labels.csv'
print('Writing to ' + output_file + '...')
f = open(output_file, 'w')
f.write(','.join(k + ':' + str(v) for k, v in labels.items()) + '\n')
f.write('Filename,Genre\n')
for path in sorted(filename_to_path.values()): #Iterate over sorted values so that the order will match prosody_labels.csv
	filename = path_to_filename[path]
	genre = None
	if filename in file_to_genre:
		genre = file_to_genre[filename]
	else:
		#This is a hack to get it to recognize composite files, since the composite files were not explicitly labeled
		for fi in file_to_genre.keys():
			if filename[:filename.rindex('.tess')] in fi: #name of the composite file is contained within the subsidiary file 
				genre = file_to_genre[fi] #copy the genre of the subsidiary file
				break
	assert genre is not None
	f.write(filename_to_path[filename] + ',' + str(labels[genre]) + '\n')
print('Success!')
