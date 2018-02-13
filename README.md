Parsing Ancient Greek texts to extract and quantify features.

Python 3.6.0

Dependencies:
pip install cltk

In order to use cltk utilities, cltk must download a Github repository onto your filesystem at ~/cltk\_data/greek/model/greek\_models\_cltk
The repository is from https://github.com/cltk/greek\_models\_cltk.git

To have cltk auto-install everything it needs, run the following commands in the python interpreter. The last command may take a few moments to complete.

from cltk.corpus.utils.importer import CorpusImporter
corpus\_importer = CorpusImporter('greek')
corpus\_importer.import\_corpus('greek\_models\_cltk')

