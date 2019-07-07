# Genre Classifier
We are data mining a corpus of ancient texts to train machine learning classifiers that distinguish between different genres.

## Setup (Instructions for Mac)

Open the Terminal app

Check if you have Python 3.6 installed:
```bash
which python3.6
```
If it is installed, this command should have output a path. For example: `/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6`. If nothing was output, download Python 3.6 here: https://www.python.org/downloads/release/python-368/

Ensure that you have the Xcode command-line tools installed on your Mac by running the `git` command in terminal:
```bash
git
```
If the command outputs information about how to use `git`, then you already have it installed. If a dialog box appears that prompts you to install, then click `Install`.

Check that you have `brew` installed:
```bash
which brew
```
If it is installed, this command should have output the following path: `/usr/local/bin/brew`. If nothing was output, install brew with the following command: 
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Install pipenv:
```bash
brew install pipenv
```

(Optional) Set environment variable by executing the following lines (which will modify `~/.bash_profile`). This should only ever need to be done once.
```bash
echo "#When pipenv makes a virtual environment, it will create it in the same directory as the project instead of ~/.local/share/virtualenv/" >> ~/.bash_profile
echo "PIPENV_VENV_IN_PROJECT=true" >> ~/.bash_profile
echo "export PIPENV_VENV_IN_PROJECT" >> ~/.bash_profile
```
Close terminal, then repoen terminal

Clone this repository - click on green 'clone' button on right side of github webpage for this repo to copy the link:
```bash
git clone <link you just copied>
```

Navigate inside the project folder:
```bash
cd <the project folder you just cloned>
```

Create/Enter virtual environment:
```bash
pipenv shell
```

Install dependencies: 
```bash
pipenv install
```

Run the demo (this does a feature extraction for a small sample of files, and analyzes the results in one step):
```bash
python demo.py
```

Extract features from all files:
```bash
python run_feature_extraction.py all_data.pickle
```

Extract features from only drama and epic files:
```bash
python run_feature_extraction.py drama_epic_data.pickle drama epic
```

Run all model analyzer functions on the data from all files to classify prose from verse:
```bash
python run_ml_analyzers.py all_data.pickle labels/prosody_labels.csv all
```

Run all model analyzer functions on the data from only drama and epic files to classify drama from epic:
```bash
python run_ml_analyzers.py drama_epic_data.pickle labels/genre_labels.csv all
```

To leave the virtual environment, use 
```bash
exit
```

To start the virtual environment again, use 
```bash
pipenv shell
```
