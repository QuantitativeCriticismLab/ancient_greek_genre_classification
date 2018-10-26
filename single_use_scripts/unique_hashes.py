from extract_features import _get_filenames
import os

"""
Number of filenames: 816
Number of unique hashes: 781
Number of unique trimmed names: 788
"""
def display_quantities(filenames):
	print('Number of filenames: ' + str(len(filenames)))
	hashes = set(hash(open(f, mode='r').read()) for f in filenames)
	print('Number of unique hashes: ' + str(len(hashes)))
	trimmed_names = {f[f.rindex(os.sep) + 1: f.rindex('.tess')] for f in filenames}
	print('Number of unique trimmed names: ' + str(len(trimmed_names)))

"""
tesserae/texts/grc/galen.natural_faculties/galen.natural_faculties.tess
tesserae/texts/grc/plato.statesman.tess
tesserae/texts/grc/plutarch.epitome_argumenti_stoicos.tess
tesserae/texts/grc/plutarch.epitome_libri_de_animae_procreatione.tess
tesserae/texts/grc/plutarch/plutarch.adversus_colotem.tess
tesserae/texts/grc/plutarch/plutarch.aemilius_paulus.tess
tesserae/texts/grc/plutarch/plutarch.agesilaus.tess
tesserae/texts/grc/plutarch/plutarch.agis.tess
tesserae/texts/grc/plutarch/plutarch.alcibiades.tess
tesserae/texts/grc/plutarch/plutarch.alexander.tess
tesserae/texts/grc/plutarch/plutarch.amatoriae_narrationes.tess
tesserae/texts/grc/plutarch/plutarch.amatorius.tess
tesserae/texts/grc/plutarch/plutarch.de_alexandri_magni_fortuna_aut_virtute.tess
tesserae/texts/grc/plutarch/plutarch.de_amicorum_multitudine.tess
tesserae/texts/grc/plutarch/plutarch.de_amore_prolis.tess
tesserae/texts/grc/plutarch/plutarch.de_animae_procreatione_in_timaeo.tess
tesserae/texts/grc/plutarch/plutarch.de_capienda_ex_inimicis_utilitate.tess
tesserae/texts/grc/plutarch/plutarch.de_cohibenda_ira.tess
tesserae/texts/grc/plutarch/plutarch.de_communibus_notitiis_adversus_stoicos .tess
tesserae/texts/grc/plutarch/plutarch.de_cupiditate_divitiarum.tess
tesserae/texts/grc/plutarch/plutarch.de_curiositate.tess
tesserae/texts/grc/plutarch/plutarch.parallela_minora .tess
tesserae/texts/grc/plutarch/plutarch.pelopidas.tess
tesserae/texts/grc/plutarch/plutarch.pericles.tess
tesserae/texts/grc/plutarch/plutarch.philopoemen.tess
tesserae/texts/grc/plutarch/plutarch.phocion.tess
tesserae/texts/grc/plutarch/plutarch.pompey.tess
tesserae/texts/grc/plutarch/plutarch.praecepta_gerendae_reipublicae.tess
tesserae/texts/grc/plutarch/plutarch.publicola.tess
tesserae/texts/grc/plutarch/plutarch.quaestiones_convivales.tess
tesserae/texts/grc/plutarch/plutarch.questiones_graecae.tess
tesserae/texts/grc/plutarch/plutarch.questiones_romanae.tess
tesserae/texts/grc/plutarch/plutarch.quomodo_adolescens_poetas_audire_debeat.tess
tesserae/texts/grc/plutarch/plutarch.quomodo_adulator_ab_amico_internoscatur.tess
tesserae/texts/grc/plutarch/plutarch.quomodo_quis_suos_in_virtute_sentiat_profectus.tess
"""
def display_hash_collisions(filenames):
	s = set()
	dup = []
	for name in filenames:
		h = hash(open(name).read())
		if h in s:
			dup.append(name)
		s.add(h)
	print('\n'.join(dup))

"""
tesserae/texts/grc/galen.natural_faculties/galen.natural_faculties.tess
tesserae/texts/grc/plutarch/plutarch.adversus_colotem.tess
tesserae/texts/grc/plutarch/plutarch.aemilius_paulus.tess
tesserae/texts/grc/plutarch/plutarch.agesilaus.tess
tesserae/texts/grc/plutarch/plutarch.agis.tess
tesserae/texts/grc/plutarch/plutarch.alcibiades.tess
tesserae/texts/grc/plutarch/plutarch.alexander.tess
tesserae/texts/grc/plutarch/plutarch.amatoriae_narrationes.tess
tesserae/texts/grc/plutarch/plutarch.amatorius.tess
tesserae/texts/grc/plutarch/plutarch.de_alexandri_magni_fortuna_aut_virtute.tess
tesserae/texts/grc/plutarch/plutarch.de_amicorum_multitudine.tess
tesserae/texts/grc/plutarch/plutarch.de_amore_prolis.tess
tesserae/texts/grc/plutarch/plutarch.de_animae_procreatione_in_timaeo.tess
tesserae/texts/grc/plutarch/plutarch.de_capienda_ex_inimicis_utilitate.tess
tesserae/texts/grc/plutarch/plutarch.de_cohibenda_ira.tess
tesserae/texts/grc/plutarch/plutarch.de_cupiditate_divitiarum.tess
tesserae/texts/grc/plutarch/plutarch.de_curiositate.tess
tesserae/texts/grc/plutarch/plutarch.pelopidas.tess
tesserae/texts/grc/plutarch/plutarch.pericles.tess
tesserae/texts/grc/plutarch/plutarch.philopoemen.tess
tesserae/texts/grc/plutarch/plutarch.phocion.tess
tesserae/texts/grc/plutarch/plutarch.pompey.tess
tesserae/texts/grc/plutarch/plutarch.praecepta_gerendae_reipublicae.tess
tesserae/texts/grc/plutarch/plutarch.publicola.tess
tesserae/texts/grc/plutarch/plutarch.quaestiones_convivales.tess
tesserae/texts/grc/plutarch/plutarch.quomodo_adolescens_poetas_audire_debeat.tess
tesserae/texts/grc/plutarch/plutarch.quomodo_adulator_ab_amico_internoscatur.tess
tesserae/texts/grc/plutarch/plutarch.quomodo_quis_suos_in_virtute_sentiat_profectus.tess
"""
def display_filename_collisions(filenames):
	s = set()
	dup = []
	for name in filenames:
		n = name[name.rindex(os.sep) + 1: name.rindex('.tess')]
		if n in s:
			dup.append(name)
		s.add(n)
	print('\n'.join(dup))

"""
There are 35 pairs of Greek files that have identical content.
{'tesserae/texts/grc/galen.natural_faculties/galen.natural_faculties.tess', 'tesserae/texts/grc/galen.natural_faculties.tess'}
{'tesserae/texts/grc/plato.politicus.tess', 'tesserae/texts/grc/plato.statesman.tess'}
{'tesserae/texts/grc/plutarch.adversus_colotem.tess', 'tesserae/texts/grc/plutarch/plutarch.adversus_colotem.tess'}
{'tesserae/texts/grc/plutarch/plutarch.aemilius_paulus.tess', 'tesserae/texts/grc/plutarch.aemilius_paulus.tess'}
{'tesserae/texts/grc/plutarch/plutarch.agesilaus.tess', 'tesserae/texts/grc/plutarch.agesilaus.tess'}
{'tesserae/texts/grc/plutarch/plutarch.agis.tess', 'tesserae/texts/grc/plutarch.agis.tess'}
{'tesserae/texts/grc/plutarch/plutarch.alcibiades.tess', 'tesserae/texts/grc/plutarch.alcibiades.tess'}
{'tesserae/texts/grc/plutarch/plutarch.alexander.tess', 'tesserae/texts/grc/plutarch.alexander.tess'}
{'tesserae/texts/grc/plutarch.amatoriae_narrationes.tess', 'tesserae/texts/grc/plutarch/plutarch.amatoriae_narrationes.tess'}
{'tesserae/texts/grc/plutarch/plutarch.amatorius.tess', 'tesserae/texts/grc/plutarch.amatorius.tess'}
{'tesserae/texts/grc/plutarch.epitome_argumenti_stoicos.tess', 'tesserae/texts/grc/plutarch.compendium_argumenti_stoicos_absurdiora_poetis_dicere.tess'}
{'tesserae/texts/grc/plutarch.epitome_libri_de_animae_procreatione.tess', 'tesserae/texts/grc/plutarch.compendium_libri_de_animae_procreatione_in_timaeo.tess'}
{'tesserae/texts/grc/plutarch.de_alexandri_magni_fortuna_aut_virtute.tess', 'tesserae/texts/grc/plutarch/plutarch.de_alexandri_magni_fortuna_aut_virtute.tess'}
{'tesserae/texts/grc/plutarch.de_amicorum_multitudine.tess', 'tesserae/texts/grc/plutarch/plutarch.de_amicorum_multitudine.tess'}
{'tesserae/texts/grc/plutarch/plutarch.de_amore_prolis.tess', 'tesserae/texts/grc/plutarch.de_amore_prolis.tess'}
{'tesserae/texts/grc/plutarch.de_animae_procreatione_in_timaeo.tess', 'tesserae/texts/grc/plutarch/plutarch.de_animae_procreatione_in_timaeo.tess'}
{'tesserae/texts/grc/plutarch/plutarch.de_capienda_ex_inimicis_utilitate.tess', 'tesserae/texts/grc/plutarch.de_capienda_ex_inimicis_utilitate.tess'}
{'tesserae/texts/grc/plutarch/plutarch.de_cohibenda_ira.tess', 'tesserae/texts/grc/plutarch.de_cohibenda_ira.tess'}
{'tesserae/texts/grc/plutarch/plutarch.de_communibus_notitiis_adversus_stoicos .tess', 'tesserae/texts/grc/plutarch.de_communibus_notitiis_adversus_stoicos.tess'}
{'tesserae/texts/grc/plutarch.de_cupiditate_divitiarum.tess', 'tesserae/texts/grc/plutarch/plutarch.de_cupiditate_divitiarum.tess'}
{'tesserae/texts/grc/plutarch/plutarch.de_curiositate.tess', 'tesserae/texts/grc/plutarch.de_curiositate.tess'}
{'tesserae/texts/grc/plutarch.parallela_minora.tess', 'tesserae/texts/grc/plutarch/plutarch.parallela_minora .tess'}
{'tesserae/texts/grc/plutarch.pelopidas.tess', 'tesserae/texts/grc/plutarch/plutarch.pelopidas.tess'}
{'tesserae/texts/grc/plutarch.pericles.tess', 'tesserae/texts/grc/plutarch/plutarch.pericles.tess'}
{'tesserae/texts/grc/plutarch/plutarch.philopoemen.tess', 'tesserae/texts/grc/plutarch.philopoemen.tess'}
{'tesserae/texts/grc/plutarch.phocion.tess', 'tesserae/texts/grc/plutarch/plutarch.phocion.tess'}
{'tesserae/texts/grc/plutarch.pompey.tess', 'tesserae/texts/grc/plutarch/plutarch.pompey.tess'}
{'tesserae/texts/grc/plutarch/plutarch.praecepta_gerendae_reipublicae.tess', 'tesserae/texts/grc/plutarch.praecepta_gerendae_reipublicae.tess'}
{'tesserae/texts/grc/plutarch.publicola.tess', 'tesserae/texts/grc/plutarch/plutarch.publicola.tess'}
{'tesserae/texts/grc/plutarch.quaestiones_convivales.tess', 'tesserae/texts/grc/plutarch/plutarch.quaestiones_convivales.tess'}
{'tesserae/texts/grc/plutarch.quaestiones_graecae.tess', 'tesserae/texts/grc/plutarch/plutarch.questiones_graecae.tess'}
{'tesserae/texts/grc/plutarch.quaestiones_romanae.tess', 'tesserae/texts/grc/plutarch/plutarch.questiones_romanae.tess'}
{'tesserae/texts/grc/plutarch/plutarch.quomodo_adolescens_poetas_audire_debeat.tess', 'tesserae/texts/grc/plutarch.quomodo_adolescens_poetas_audire_debeat.tess'}
{'tesserae/texts/grc/plutarch/plutarch.quomodo_adulator_ab_amico_internoscatur.tess', 'tesserae/texts/grc/plutarch.quomodo_adulator_ab_amico_internoscatur.tess'}
{'tesserae/texts/grc/plutarch.quomodo_quis_suos_in_virtute_sentiat_profectus.tess', 'tesserae/texts/grc/plutarch/plutarch.quomodo_quis_suos_in_virtute_sentiat_profectus.tess'}

Of these 35 pairs, 7 of them don't even have the same names so they are hard to catch.
{'tesserae/texts/grc/plato.politicus.tess', 'tesserae/texts/grc/plato.statesman.tess'}
{'tesserae/texts/grc/plutarch.epitome_argumenti_stoicos.tess', 'tesserae/texts/grc/plutarch.compendium_argumenti_stoicos_absurdiora_poetis_dicere.tess'}
{'tesserae/texts/grc/plutarch.epitome_libri_de_animae_procreatione.tess', 'tesserae/texts/grc/plutarch.compendium_libri_de_animae_procreatione_in_timaeo.tess'}
{'tesserae/texts/grc/plutarch/plutarch.de_communibus_notitiis_adversus_stoicos .tess', 'tesserae/texts/grc/plutarch.de_communibus_notitiis_adversus_stoicos.tess'}
{'tesserae/texts/grc/plutarch.parallela_minora.tess', 'tesserae/texts/grc/plutarch/plutarch.parallela_minora .tess'}
{'tesserae/texts/grc/plutarch.quaestiones_graecae.tess', 'tesserae/texts/grc/plutarch/plutarch.questiones_graecae.tess'}
{'tesserae/texts/grc/plutarch.quaestiones_romanae.tess', 'tesserae/texts/grc/plutarch/plutarch.questiones_romanae.tess'}
"""
def display_filename_collisions_dict(filenames):
	d = {}
	for name in filenames:
		d[name] = hash(open(name).read())
	rev_multidict = {}
	for key, value in d.items():
		rev_multidict.setdefault(value, set()).add(key)
	print('\n'.join([str(values) for key, values in rev_multidict.items() if len(values) > 1]))

def display_non_duplicate_plutarch(filenames):
	d = {}
	for name in filenames:
		d[name] = hash(open(name).read())
	rev_multidict = {}
	for key, value in d.items():
		rev_multidict.setdefault(value, set()).add(key)

	dup_names = (v for k, v in rev_multidict.items() if len(v) > 1)
	dup_plutarch_filenames = []
	for duplicates in dup_names:
		for elem in duplicates:
			if elem.startswith('tesserae/texts/grc/plutarch/'):
				dup_plutarch_filenames.append(elem)
	dup_plutarch_filenames = sorted(dup_plutarch_filenames)
	plutarch_filenames = sorted(_get_filenames('tesserae/texts/grc/plutarch', 'tess', set()))

	#Prints files in the plutarch directory that have been identified as duplicates
	print('\n'.join(dup_plutarch_filenames))
	print()

	#Prints all files in the plutarch directory
	print('\n'.join(plutarch_filenames))

if __name__ == '__main__':
	filenames = _get_filenames('tesserae/texts/grc', 'tess', set())
	display_non_duplicate_plutarch(filenames)

#This is the issue I posted to the tesserae repo as issue #57
'''
There are 36 files that should be discarded because there are duplicates.

The entire directory of 32 files in `tesserae/texts/grc/plutarch/` should be discarded. Of the 32 files in `tesserae/texts/grc/plutarch/`, 27 of them have an identical name _**and**_ content to a file one directory above in `tesserae/texts/grc/`.
```
{'tesserae/texts/grc/plutarch.adversus_colotem.tess', 'tesserae/texts/grc/plutarch/plutarch.adversus_colotem.tess'}
{'tesserae/texts/grc/plutarch/plutarch.aemilius_paulus.tess', 'tesserae/texts/grc/plutarch.aemilius_paulus.tess'}
{'tesserae/texts/grc/plutarch/plutarch.agesilaus.tess', 'tesserae/texts/grc/plutarch.agesilaus.tess'}
{'tesserae/texts/grc/plutarch/plutarch.agis.tess', 'tesserae/texts/grc/plutarch.agis.tess'}
{'tesserae/texts/grc/plutarch/plutarch.alcibiades.tess', 'tesserae/texts/grc/plutarch.alcibiades.tess'}
{'tesserae/texts/grc/plutarch/plutarch.alexander.tess', 'tesserae/texts/grc/plutarch.alexander.tess'}
{'tesserae/texts/grc/plutarch.amatoriae_narrationes.tess', 'tesserae/texts/grc/plutarch/plutarch.amatoriae_narrationes.tess'}
{'tesserae/texts/grc/plutarch/plutarch.amatorius.tess', 'tesserae/texts/grc/plutarch.amatorius.tess'}
{'tesserae/texts/grc/plutarch.de_alexandri_magni_fortuna_aut_virtute.tess', 'tesserae/texts/grc/plutarch/plutarch.de_alexandri_magni_fortuna_aut_virtute.tess'}
{'tesserae/texts/grc/plutarch.de_amicorum_multitudine.tess', 'tesserae/texts/grc/plutarch/plutarch.de_amicorum_multitudine.tess'}
{'tesserae/texts/grc/plutarch/plutarch.de_amore_prolis.tess', 'tesserae/texts/grc/plutarch.de_amore_prolis.tess'}
{'tesserae/texts/grc/plutarch.de_animae_procreatione_in_timaeo.tess', 'tesserae/texts/grc/plutarch/plutarch.de_animae_procreatione_in_timaeo.tess'}
{'tesserae/texts/grc/plutarch/plutarch.de_capienda_ex_inimicis_utilitate.tess', 'tesserae/texts/grc/plutarch.de_capienda_ex_inimicis_utilitate.tess'}
{'tesserae/texts/grc/plutarch/plutarch.de_cohibenda_ira.tess', 'tesserae/texts/grc/plutarch.de_cohibenda_ira.tess'}
{'tesserae/texts/grc/plutarch/plutarch.de_communibus_notitiis_adversus_stoicos .tess', 'tesserae/texts/grc/plutarch.de_communibus_notitiis_adversus_stoicos.tess'}
{'tesserae/texts/grc/plutarch.de_cupiditate_divitiarum.tess', 'tesserae/texts/grc/plutarch/plutarch.de_cupiditate_divitiarum.tess'}
{'tesserae/texts/grc/plutarch/plutarch.de_curiositate.tess', 'tesserae/texts/grc/plutarch.de_curiositate.tess'}
{'tesserae/texts/grc/plutarch.parallela_minora.tess', 'tesserae/texts/grc/plutarch/plutarch.parallela_minora .tess'}
{'tesserae/texts/grc/plutarch.pelopidas.tess', 'tesserae/texts/grc/plutarch/plutarch.pelopidas.tess'}
{'tesserae/texts/grc/plutarch.pericles.tess', 'tesserae/texts/grc/plutarch/plutarch.pericles.tess'}
{'tesserae/texts/grc/plutarch/plutarch.philopoemen.tess', 'tesserae/texts/grc/plutarch.philopoemen.tess'}
{'tesserae/texts/grc/plutarch.phocion.tess', 'tesserae/texts/grc/plutarch/plutarch.phocion.tess'}
{'tesserae/texts/grc/plutarch.pompey.tess', 'tesserae/texts/grc/plutarch/plutarch.pompey.tess'}
{'tesserae/texts/grc/plutarch/plutarch.praecepta_gerendae_reipublicae.tess', 'tesserae/texts/grc/plutarch.praecepta_gerendae_reipublicae.tess'}
{'tesserae/texts/grc/plutarch.publicola.tess', 'tesserae/texts/grc/plutarch/plutarch.publicola.tess'}
{'tesserae/texts/grc/plutarch.quaestiones_convivales.tess', 'tesserae/texts/grc/plutarch/plutarch.quaestiones_convivales.tess'}
{'tesserae/texts/grc/plutarch.quaestiones_graecae.tess', 'tesserae/texts/grc/plutarch/plutarch.questiones_graecae.tess'}
{'tesserae/texts/grc/plutarch.quaestiones_romanae.tess', 'tesserae/texts/grc/plutarch/plutarch.questiones_romanae.tess'}
{'tesserae/texts/grc/plutarch/plutarch.quomodo_adolescens_poetas_audire_debeat.tess', 'tesserae/texts/grc/plutarch.quomodo_adolescens_poetas_audire_debeat.tess'}
{'tesserae/texts/grc/plutarch/plutarch.quomodo_adulator_ab_amico_internoscatur.tess', 'tesserae/texts/grc/plutarch.quomodo_adulator_ab_amico_internoscatur.tess'}
{'tesserae/texts/grc/plutarch.quomodo_quis_suos_in_virtute_sentiat_profectus.tess', 'tesserae/texts/grc/plutarch/plutarch.quomodo_quis_suos_in_virtute_sentiat_profectus.tess'}
```

Of the remaining 5 files in `tesserae/texts/grc/plutarch/`, 4 of them have identical content _**but not**_ an identical name to some file one directory above in `tesserae/texts/grc/` (two pairs of these files have an _almost_ identical name but there is a space between the file name and the `.tess` extension).

```
{'tesserae/texts/grc/plutarch/plutarch.de_communibus_notitiis_adversus_stoicos .tess', 'tesserae/texts/grc/plutarch.de_communibus_notitiis_adversus_stoicos.tess'}
{'tesserae/texts/grc/plutarch.parallela_minora.tess', 'tesserae/texts/grc/plutarch/plutarch.parallela_minora .tess'}
{'tesserae/texts/grc/plutarch.quaestiones_graecae.tess', 'tesserae/texts/grc/plutarch/plutarch.questiones_graecae.tess'}
{'tesserae/texts/grc/plutarch.quaestiones_romanae.tess', 'tesserae/texts/grc/plutarch/plutarch.questiones_romanae.tess'}
```

The remaining 1 file in `tesserae/texts/grc/plutarch/` is `tesserae/texts/grc/plutarch/plutarch_amatorius.tess`. I mentioned it in an earlier comment because its naming schema is off. It has neither an identical name nor identical content to a file above in `tesserae/texts/grc/`. However it is _**almost**_ completely identical to `tesserae/texts/grc/plutarch/plutarch.amatorius.tess` and `tesserae/texts/grc/plutarch.amatorius.tess`. The only difference is the `tess` tags - the actual Greek is completely identical.

There are two pairs of plutarch files *outside* of `tesserae/texts/grc/plutarch/` that are identical to each other, bringing our duplicate count to 34.
```
{'tesserae/texts/grc/plutarch.epitome_argumenti_stoicos.tess', 'tesserae/texts/grc/plutarch.compendium_argumenti_stoicos_absurdiora_poetis_dicere.tess'}
{'tesserae/texts/grc/plutarch.epitome_libri_de_animae_procreatione.tess', 'tesserae/texts/grc/plutarch.compendium_libri_de_animae_procreatione_in_timaeo.tess'}
```

There are another two pairs of identical files that are not related to plutarch. This brings our count of duplicate files to 36
```
{'tesserae/texts/grc/galen.natural_faculties/galen.natural_faculties.tess', 'tesserae/texts/grc/galen.natural_faculties.tess'}
{'tesserae/texts/grc/plato.politicus.tess', 'tesserae/texts/grc/plato.statesman.tess'}
```
'''
