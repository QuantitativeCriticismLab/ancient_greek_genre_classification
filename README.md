# Greek Prose Classifier
Data mining a corpus of Ancient Greek texts to train machine learning classifiers that distinguish poetry from prose.

## Setup (Instructions for Mac)
Install Homebrew:
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Install pipenv: `brew install pipenv`

Set environment variable by placing the following lines in `~/.bash_profile` (optional)
```bash
echo "#When pipenv makes a virtual environment, it will create it in the same directory as the project instead of ~/.local/share/virtualenv/" >> ~/.bash_profile
echo "PIPENV_VENV_IN_PROJECT=true" >> ~/.bash_profile
echo "export PIPENV_VENV_IN_PROJECT" >> ~/.bash_profile
```
Close terminal, then repoen

Clone this repository: `git clone <this repo>`

Navigate inside the repository: `cd <this directory>`

Enter virtual environment: `pipenv shell`

Install dependencies: `pipenv install`

In order to use cltk utilities, cltk must download a Github repository onto your filesystem (on Mac, it's at ~/cltk\_data/greek/model/greek\_models\_cltk) The repository is from https://github.com/cltk/greek_models_cltk.git. You can have cltk install this automatically. To have cltk auto-install everything it needs, run the following commands in the python interpreter. To start the python interpreter just run the command `python` in your shell.

```
>>> from cltk.corpus.utils.importer import CorpusImporter
>>> corpus_importer = CorpusImporter('greek')
>>> corpus_importer.import_corpus('greek_models_cltk')
```

To leave the virtual environment, use `exit`

To start the virtual environment again, use `pipenv shell`
