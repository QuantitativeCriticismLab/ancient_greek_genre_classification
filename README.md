# Greek Genre Classifier
We are data mining a corpus of ancient texts to train machine learning classifiers that distinguish between different genres.

## Setup

1. Ensure you have `git` installed with version<sup id="a0">[0](#f0)</sup> at least `1.9`.
1. This project requires a certain version of `Python`. You can find this version by running the following command from the project directory:
	```bash
	grep 'python_version' Pipfile | cut -f 2 -d '"'
	```
	To determine whether this version is installed on your system, run:
	```bash
	which python`grep 'python_version' Pipfile | cut -f 2 -d '"'`
	```
	If the version is already installed, a path will be output (e.g. /Library/Frameworks/Python.framework/Versions/3.x/bin/python3.x). If nothing was output, then you don't have the necessary version of `Python` installed. You can install it [here](https://www.python.org/downloads/).
1. Ensure `pipenv`<sup id="a1">[1](#f1)</sup> is already installed by using:
	```bash
	which pipenv
	```
	If no path is output, then install `pipenv` with:
	```bash
	pip3 install pipenv
	```
1. While in the project directory, run the following command. This will generate a virtual environment called `.venv/` in the current directory<sup id="a2">[2](#f2)</sup> that will contain all<sup id="a3">[3](#f3)</sup> the `Python` dependencies for this project.
	```bash
	PIPENV_VENV_IN_PROJECT=true pipenv install --dev
	```
1. The following command will activate the virtual environment. After activation, running `Python` commands will ignore the system-level `Python` version & packages, and only use the version & packages from the virtual environment.
	```bash
	pipenv shell
	```

Using `exit` will exit the virtual environment i.e. it restores the system-level `Python` configurations to your shell. Whenever you want to resume working on the project, run `pipenv shell` while in the project directory to activate the virtual environment again.

Use `pipenv check` to ensure that your `Pipfile` and `Pipfile.lock` are in sync. If there is some discrepancy or you lack dependencies, then run `pipenv install --dev` while your virtual environment is activated. This should ensure that your project has all the necessary dependencies.

## Development

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

## Footnotes

<b id="f0">0)</b> The project uses the `git` protocol to download the corpus. We make use of `git`'s sparse checkout and shallow clone features to download only what we need from the repository (this is done automatically in the code). We must have [at least `git` version 1.9 to perform a sparse checkout and shallow clone](https://stackoverflow.com/a/28039894/7102572).[↩](#a0)

<b id="f1">1)</b> The `pipenv` tool works by making a project-specific directory called a virtual environment that hold the dependencies for that project. After a virtual environment is activated, newly installed dependencies will automatically go into the virtual environment instead of being placed among your system-level `Python` packages. This precludes the possiblity of different projects on the same machine from having dependencies that conflict with one another. [↩](#a1)

<b id="f2">2)</b> Setting the `PIPENV_VENV_IN_PROJECT` variable to true will indicate to `pipenv` to make this virtual environment within the same directory as the project so that all the files corresponding to a project can be in the same place. This is [not default behavior](https://github.com/pypa/pipenv/issues/1382) (e.g. on Mac, the environments will normally be placed in `~/.local/share/virtualenvs/` by default). [↩](#a2)

<b id="f3">3)</b> Using `--dev` ensures that even development dependencies will be installed (dev dependencies may include testing and linting frameworks which are not necessary for normal execution of the code). `Pipfile.lock` specifies the packages and exact versions (for both dev dependencies and regular dependencies) for the virtual environment. After installation, you can find all dependencies in `<path to virtual environment>/lib/python<python version>/site-packages/`. [↩](#a3)
