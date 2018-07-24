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

To leave the virtual environment, use `exit`

To start the virtual environment again, use `pipenv shell`
