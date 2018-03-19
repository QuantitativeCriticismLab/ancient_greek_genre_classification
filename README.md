Parsing Ancient Greek texts to extract and quantify features.

Python 3.6.0

Dependencies:
pip install cltk

In order to use cltk utilities, cltk must download a Github repository onto your filesystem (on Mac, it's at ~/cltk\_data/greek/model/greek\_models\_cltk) The repository is from https://github.com/cltk/greek_models_cltk.git. You can have cltk install this automatically.

To have cltk auto-install everything it needs, run the following commands in the python interpreter. To start the python interpreter just run the command `python` in your shell.

```
>>> from cltk.corpus.utils.importer import CorpusImporter
>>> corpus_importer = CorpusImporter('greek')
>>> corpus_importer.import_corpus('greek_models_cltk')
```
