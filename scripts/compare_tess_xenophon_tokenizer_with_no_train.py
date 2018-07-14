import os
from cltk.utils.file_operations import open_pickle
from nltk.tokenize.punkt import PunktLanguageVars, PunktTrainer, PunktSentenceTokenizer
from progress_bar import print_progress_bar
from extract_features import parse_tess, file_parsers

PunktLanguageVars.sent_end_chars = ('.', ';', ';')
PunktLanguageVars.internal_punctuation = (',', '·', ':')

notrain_tokenizer = PunktSentenceTokenizer()
tess_tokenizer = PunktSentenceTokenizer(parse_tess('tesserae/texts/grc/xenophon.anabasis.tess'))

corpus_dir = 'tesserae' + os.sep + 'texts' + os.sep + 'grc'
file_extension = 'tess'

#Obtain all the files to parse by traversing through the directory
file_names = sorted(list({current_path + os.sep + current_file_name for current_path, current_dir_names, current_file_names in \
os.walk(corpus_dir) for current_file_name in current_file_names if current_file_name.endswith('.' + file_extension)}))

n_file = open('notes/notrain_sentences.txt', mode='w')
t_file = open('notes/tesstrain_sentences.txt', mode='w')
counter = 1
for file_name in file_names:
	file_text = file_parsers[file_extension](file_name)
	n_tokens = notrain_tokenizer.tokenize(file_text)
	t_tokens = tess_tokenizer.tokenize(file_text)
	if n_tokens != t_tokens:
		n_file.write(file_name + '\n' + '\n'.join(n_tokens) + '\n\n')
		t_file.write(file_name + '\n' + '\n'.join(t_tokens) + '\n\n')
	print_progress_bar(counter, len(file_names))
	counter += 1

'''
Most of the instances of a period followed by no space are a parsing errors on the part of tesserae from the original Perseus xml

Observe line 151 from aeschines.against_ctesiphon.tess

<aeschin. 1.151> ὁ τοίνυν οὐδενὸς ἧττον σοφὸς τῶν ποιητῶν Εὐριπίδης, ἕν τι τῶν καλλίστων ὑπολαμβάνων εἶναι τὸ σωφρόνως ἐρᾶν, ἐν εὐχῆς μέρει τὸν ἔρωτα ποιούμενος λέγει που:  ὁ δ' εἰς τὸ σῶφρον ἐπ' ἀρετήν τ' ἄγων ἔρωσζηλωτὸς ἀνθρώποισιν, ὧν εἴην ἐγώ.ευριπιδες, στηενοβοεα: ναυξκ 672.

There is no space between "ἐγώ.ευριπιδες". However, in the Perseus xml the "ευριπιδες, στηενοβοεα: ναυξκ 672." is part of a <bibl> tag that isn't omitted properly

<div2 type="section" n="151" org="uniform" sample="complete"><p>o( toi/nun ou)deno\s h(=tton sofo\s tw=n poihtw=n *eu)ripi/dhs, e(/n ti tw=n kalli/stwn u(polamba/nwn ei)=nai to\ swfro/nws e)ra=n, e)n eu)xh=s me/rei to\n e)/rwta poiou/menos le/gei pou: <cit><quote type="verse"><l met="iambic"> o( d' ei)s to\ sw=fron e)p' a)reth/n t' a)/gwn e)/rws</l><l>zhlwto\s a)nqrw/poisin, w(=n ei)/hn e)gw/.</l></quote><bibl default="NO">Euripides, Sthenoboea: Nauck 672.</bibl></cit></p></div2>



I ran the following command, comparing the output of a tokenizer that was not trained vs a tokenizer that was trained on xenophon.anabasis.tess from the tesserae corpus.

diff notes/notrain_sentences.txt notes/tesstrain_sentences.txt > notes/notrain_tess.diff


One difference between the tokenizers is in Apollodorus's Epitome where the former tokenizer didn't cut the sentence after "... καὶ Θέτιδος ν. ἐκ Φυλάκης ..." The "ν." is not an abbreviation, but the Greek number fifty followed by a period - therefore it should have cut the sentence.

The latter tokenizer makes the same mistakes of assuming a number is an abbreviation if it is the last word in the sentence (e.g. "... Αστυόχης ναῦς θ.", "... Χαρόπου ναῦς γ."), it just seems to make this mistake slightly less often.

notrain_tess.diff
1967c1969,1970
< ̔Ροδίων Τληπόλεμος ̔Ηρακλέους καὶ ̓Αστυόχης ναῦς θ. Συμαίων Νιρεὺς Χαρόπου ναῦς γ. Κώων Φείδιππος καὶ ̓́Αντιφος οἱ Θεσσαλοῦ λ. Μυρμιδόνων ̓Αχιλλεὺς Πηλέως καὶ Θέτιδος ν. ἐκ Φυλάκης Πρωτεσίλαος ̓Ιφίκλου μ. Φεραίων Εὔμηλος ̓Αδμήτου ια.
---
> ̔Ροδίων Τληπόλεμος ̔Ηρακλέους καὶ ̓Αστυόχης ναῦς θ. Συμαίων Νιρεὺς Χαρόπου ναῦς γ. Κώων Φείδιππος καὶ ̓́Αντιφος οἱ Θεσσαλοῦ λ. Μυρμιδόνων ̓Αχιλλεὺς Πηλέως καὶ Θέτιδος ν.
> ἐκ Φυλάκης Πρωτεσίλαος ̓Ιφίκλου μ. Φεραίων Εὔμηλος ̓Αδμήτου ια.

notrain_sentences.txt
Μυρμιδόνων ̓Αχιλλεὺς Πηλέως καὶ Θέτιδος ν. ἐκ Φυλάκης Πρωτεσίλαος ̓Ιφίκλου μ. Φεραίων Εὔμηλος ̓Αδμήτου ια.

apollodorus.epitome.tess
<apollod. epit. Epitome.E.3.14> Μυρμιδόνων ̓Αχιλλεὺς Πηλέως καὶ Θέτιδος ν. ἐκ Φυλάκης Πρωτεσίλαος ̓Ιφίκλου μ. Φεραίων Εὔμηλος ̓Αδμήτου ια. ̓Ολιζώνων Φιλοκτήτης Ποίαντος ζ. Αἰνιάνων Γουνεὺς ̓Ωκύτου κβ. Τρικκαίων Ποδαλείριοσλ. ̓Ορμενίων Εὐρύπυλοσναῦς μ. Γυρτωνίων Πολυποίτης Πειρίθου λ. Μαγνήτων Πρόθοος Τενθρήδονος μ. νῆες μὲν οὖν αἱ πᾶσαι ,αιγ, ἡγεμόνες δὲ μγ, ἡγεμόνειαι δὲ λ:

From http://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0021%3Atext%3DEpitome%3Abook%3DE%3Achapter%3D3%3Asection%3D14
[14] Μυρμιδόνων Ἀχιλλεὺς Πηλέως καὶ Θέτιδος ν. ἐκ Φυλάκης Πρωτεσίλαος Ἰφίκλου μ. Φεραίων Εὔμηλος Ἀδμήτου ια. Ὀλιζώνων Φιλοκτήτης Ποίαντος ζ. Αἰνιάνων Γουνεὺς Ὠκύτου κβ. Τρικκαίων Ποδαλείριος ... λ. Ὀρμενίων Εὐρύπυλος ... ναῦς μ. Γυρτωνίων Πολυποίτης Πειρίθου λ. Μαγνήτων Πρόθοος Τενθρήδονος μ. νῆες μὲν οὖν αἱ πᾶσαι ,αιγ, ἡγεμόνες δὲ μγ, ἡγεμόνειαι δὲ λ:

From http://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0022%3Atext%3DEpitome%3Abook%3DE%3Achapter%3D3%3Asection%3D14
[14] Of the Myrmidons, Achilles, son of Peleus and Thetis: fifty ships. From Phylace, Protesilaus, son of Iphiclus: forty ships. Of the Pheraeans, Eumelus, son of Admetus: eleven ships. Of the Olizonians, Philoctetes, son of Poeas: seven ships. Of the Aeanianians, Guneus, son of Ocytus: twenty-two ships. Of the Triccaeans, Podalirius:thirty ships. Of the Ormenians, Eurypylus: forty ships. Of the Gyrtonians, Polypoetes, son of Pirithous: thirty ships. Of the Magnesians, Prothous, son of Tenthredon: forty ships. The total of ships was one thousand and thirteen; of leaders, forty-three; of leaderships, thirty.

Perseus_text_1999.01.0021.xml
<milestone n="14" unit="section" />*murmido/nwn *)axilleu\s *phle/ws kai\ *qe/tidos <num lang="greek">n</num>. e)k *fula/khs *prwtesi/laos *)ifi/klou <num lang="greek">m</num>. *ferai/wn *eu)/mhlos *)admh/tou <num lang="greek">ia</num>. *)olizw/nwn *filokth/ths *poi/antos <num lang="greek">z</num>. *ai)nia/nwn *gouneu\s *)wku/tou <num lang="greek">kb</num>. *trikkai/wn *podalei/rios<gap /><num lang="greek">l</num>. *)ormeni/wn  *eu)ru/pulos<gap />nau=s <num lang="greek">m</num>. *gurtwni/wn *polupoi/ths *peiri/qou <num lang="greek">l</num>. *magnh/twn *pro/qoos *tenqrh/donos <num lang="greek">m</num>. nh=es me\n ou)=n ai( pa=sai ,<num lang="greek">aig</num>, h(gemo/nes de\ <num lang="greek">mg</num>,  h(gemo/neiai de\ <num lang="greek">l</num>:



Another instance of a parsing difference is in Aretaeus's "Curatione" after "... στῆσαι δύνασθα ι.". Again, the former tokenizer assumed that "ι." is an abbreviation, but it appears to be a form of "εἶμι" followed by a period.
http://www.perseus.tufts.edu/hopper/morph?l=I&la=greek&can=i0&prior=du/nasqa&d=Perseus:text:1999.01.0253:text=SA:book=1:chapter=6&i=1


http://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0254%3Atext%3DSA%3Abook%3D1%3Achapter%3D6

ξύνεστι μὲν αὐτέοισι, ἀθρόον μὲν εἰρῆσθαι, ἅπασι πόνος καὶ ἔντασις τενόντων καὶ Ρ῾άχεος, καὶ μυῶν τῶν ἐν γνάθοισι καὶ θώρηκι, ἐρείδουσι γὰρ τὴν κάτω γένυν πρὸς τὴν ἄνω, ὡς μηδὲ μοχλοῖσιν ἢ σφηνὶ διὰ Ρ῾ηϊδίως στῆσαι δύνασθα ι.

Here is the context of this excerpt in english:
In all these varieties, then, to speak generally, there is a pain and tension of the tendons and spine, and of the muscles connected with the jaws and cheek; for they fasten the lower jaw to the upper, so that it could not easily be separated even with levers or a wedge. But if one, by forcibly separating the teeth, pour in some liquid, the patients do not drink it but squirt it out, or retain it in the mouth, or it regurgitates by the nostrils; for the isthmus faucium is strongly compressed, and the tonsils being hard and tense, do not coalesce so as to propel that which is swallowed. The face is ruddy, and of mixed colours, the eyes almost immoveable, or are rolled about with difficulty; strong feeling of suffocation; respiration bad, distension of the arms and legs; subsultus of the muscles; the countenance variously distorted; the cheeks and lips tremulous; the jaw quivering, and the teeth rattling, and in certain rare cases even the ears are thus affected. I myself have beheld
'''
