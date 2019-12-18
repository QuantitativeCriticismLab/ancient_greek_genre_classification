# pylint: disable = C
from collections import OrderedDict

#These files are composites of files that already exist in parts in the tesserae corpus
composite_files = {
	'tesserae/texts/grc/antiphon.speeches.tess',
	'tesserae/texts/grc/apollonius.argonautica.tess',
	'tesserae/texts/grc/appian.civil_wars.tess',
	'tesserae/texts/grc/dionysius_halicarnassensis.antiquitates_romanae.tess',
	'tesserae/texts/grc/eusebius_caesarea.historia_ecclesiastica.tess',
	'tesserae/texts/grc/flavius_josephus.antiquitates_judaicae.tess',
	'tesserae/texts/grc/flavius_josephus.contra_apionem.tess',
	'tesserae/texts/grc/flavius_josephus.de_bello_judaico_libri_vii.tess',
	'tesserae/texts/grc/galen.natural_faculties.tess',
	'tesserae/texts/grc/herodotus.histories.tess',
	'tesserae/texts/grc/homer.iliad.tess',
	'tesserae/texts/grc/homer.odyssey.tess',
	'tesserae/texts/grc/hyperides.speeches.tess',
	'tesserae/texts/grc/isaeus.speeches.tess',
	'tesserae/texts/grc/isocrates.letters.tess',
	'tesserae/texts/grc/isocrates.speeches.tess',
	'tesserae/texts/grc/lysias.speeches.tess',
	'tesserae/texts/grc/nonnus_of_panopolis.dionysiaca.tess',
	'tesserae/texts/grc/oppian.halieutica.tess',
	'tesserae/texts/grc/oppian_of_apamea.cynegetica.tess',
	'tesserae/texts/grc/pausanias.description_of_greece.tess',
	'tesserae/texts/grc/philostratus_the_athenian.vita_apollonii.tess',
	'tesserae/texts/grc/pindar.odes.tess',
	'tesserae/texts/grc/plato.epistles.tess',
	'tesserae/texts/grc/plato.leges.tess',
	'tesserae/texts/grc/plato.respublica.tess',
	'tesserae/texts/grc/quintus_smyrnaeus.fall_of_troy.tess',
	'tesserae/texts/grc/strabo.geography.tess',
	'tesserae/texts/grc/thucydides.peleponnesian_war.tess',
}

def _get_categories():
	f = open('labels/genre_labels.csv')
	val_to_label = {tok.split(':')[1]: tok.split(':')[0] for tok in f.readline().strip().split(',')}
	f.readline()
	categories = OrderedDict((label, set()) for label in val_to_label.values())
	for line in f:
		line = line.strip().split(',')
		categories[val_to_label[line[1]]].add(line[0])
	return categories

genre_to_files = _get_categories()
