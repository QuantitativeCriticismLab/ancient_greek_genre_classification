# Greek Prose Classifier
Data mining a corpus of Ancient Greek texts to train machine learning classifiers that distinguish poetry from prose.

## Setup (Instructions for Mac)
Install Homebrew:
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Install pipenv: `brew install pipenv`

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

Run the demo:
```bash
python demo.py
```

To leave the virtual environment, use 
```bash
exit
```

To start the virtual environment again, use 
```bash
pipenv shell
```
