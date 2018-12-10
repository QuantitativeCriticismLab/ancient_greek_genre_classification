# Greek Prose Classifier
Data mining a corpus of Ancient Greek texts to train machine learning classifiers that distinguish different genres.

## Setup (Instructions for Mac)
Install Homebrew:
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Install pipenv:
```bash
brew install pipenv
```

(Optional) Set environment variable by executing the following lines (which will modify `~/.bash_profile`)
```bash
echo "#When pipenv makes a virtual environment, it will create it in the same directory as the project instead of ~/.local/share/virtualenv/" >> ~/.bash_profile
echo "PIPENV_VENV_IN_PROJECT=true" >> ~/.bash_profile
echo "export PIPENV_VENV_IN_PROJECT" >> ~/.bash_profile
```
Close terminal, then repoen

Clone this repository: 
```bash
git clone <this repo>
```

Navigate inside the repository: 
```bash
cd <this directory>
```

Enter virtual environment: 
```bash
pipenv shell
```

Install dependencies: 
```bash
pipenv install
```

Run the demo (this does a simple feature extraction, and analyzes the results in one step):
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
