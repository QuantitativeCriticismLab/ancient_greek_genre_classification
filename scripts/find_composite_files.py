from extract_features import _get_filenames
import os

names = _get_filenames('tesserae/texts/grc', 'tess', set())
file_names = {f[f.rindex(os.sep) + 1: f.rindex('.tess')] for f in names}

composites = set()
for f in sorted(list(file_names)):
	if '.part' in f:
		composites.add(f[:f.rindex('.part')])

composites = sorted(list(composites))
for f in composites:
	if f not in file_names:
		print(f + ' is not in the corpus')
print()
#Ensure the full path matches the results of the previous loop
for f in composites:
	f = os.path.join('tesserae', 'texts', 'grc', f) + '.tess'
	if f not in names:
		print(f + ' is not in corpus')

print()
print('\n'.join(os.path.join('tesserae', 'texts', 'grc', f) + '.tess' for f in composites))
