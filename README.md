# Greek Genre Classifier
We are data mining a corpus of ancient texts to train machine learning classifiers that distinguish between different genres.

## Setup

1. Ensure you have `git` installed with version<sup id="a0">[0](#f0)</sup> at least `1.9`.
1. Navigate to the project directory. All commands *must* be run in the project directory.
	```bash
	cd <this project directory>
	```
1. This project requires a certain version of `Python`. The following command should output the version number.
	```bash
	grep 'python_version' Pipfile | cut -f 2 -d '"'
	```
	Determine whether this version is already installed. If you are using `bash` or `zsh`, you can verify this with the following command:
	```bash
	command -v "python`grep 'python_version' Pipfile | cut -f 2 -d '"'`" &> /dev/null; if [[ $? -eq 0 ]]; then echo "$_ currently installed"; else echo "$_ NOT installed"; fi
	```
	If the version of `Python` is not installed, you can install it here: https://www.python.org/downloads/.
1. Ensure `pipenv`<sup id="a1">[1](#f1)</sup> is already installed. If you are using `bash` or `zsh`, you can verify this with the following command:
	```bash
	command -v pipenv &> /dev/null; if [[ $? -eq 0 ]]; then echo "$_ currently installed"; else echo "$_ NOT installed"; fi
	```
	If `pipenv` is not installed, then install it with:
	```bash
	pip3 install pipenv
	```
1. The following command will generate a virtual environment called `.venv/` in the current directory<sup id="a2">[2](#f2)</sup> that will contain all<sup id="a3">[3](#f3)</sup> the `Python` dependencies for this project.
	```bash
	PIPENV_VENV_IN_PROJECT=true pipenv install --dev
	```
1. Activate the virtual environment.
	```bash
	pipenv shell
	```

Using `exit` will exit the virtual environment i.e. it restores the system-level `Python` configurations to your shell. Whenever you want to resume working on the project, run `pipenv shell` while in the project directory to activate the virtual environment again.

When installing new dependencies, do *not* use `pip install <dependency name>`. Instead, use `pipenv install <dependency name>`. This is because `pipenv` updates `Pipfile` and `Pipfile.lock`, but `pip` does not. Having these files match the state of your virtual environment ensures that anyone else who starts the project will have a virtual environment that looks exactly like yours.

Use `pipenv check` to ensure that the virtual environment is in a stable condition. If not, then run `pipenv install --dev` while your virtual environment is activated. This should ensure that your project has all the necessary dependencies.

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

## Footnotes

<b id="f0">0)</b> The project uses the `git` protocol to download the corpus. We make use of `git`'s sparse checkout and shallow clone features to download only what we need from the repository (this is done automatically in the code). We must have [at least `git` version 1.9 to perform a sparse checkout and shallow clone](https://stackoverflow.com/a/28039894/7102572).[↩](#a0)

<b id="f1">1)</b> The `pipenv` tool manages project dependencies. It works by making a project-specific directory called a virtual environment that holds the dependencies for that project. After a virtual environment is "activated", `Python` commands will ignore the system-level `Python` version & dependencies. Only the version & dependencies in the virtual environment will be recognized. Also, newly installed dependencies will automatically go into the virtual environment instead of being placed among your system-level `Python` dependencies. This precludes the possiblity of different projects on the same system from having dependencies that conflict with one another. It also makes it easier to clean up after deleting a project: instead of remembering to uninstall several dependencies from your system, you can just delete the virtual environment.[↩](#a1)

<b id="f2">2)</b> Setting the `PIPENV_VENV_IN_PROJECT` variable to true will indicate to `pipenv` to make this virtual environment within the project directory so that all the files corresponding to a project can be in the same place. This is [not default behavior](https://github.com/pypa/pipenv/issues/1382) (e.g. on Mac, the environments will normally be placed in `~/.local/share/virtualenvs/` by default). [↩](#a2)

<b id="f3">3)</b> Using `--dev` ensures that even development dependencies will be installed (dev dependencies may include testing and linting frameworks which are not necessary for normal execution of the code). `Pipfile.lock` specifies the dependencies and exact versions (for both dev dependencies and regular dependencies) for the virtual environment. After installation, you can find all dependencies in `<path to virtual environment>/lib/python<python version>/site-packages/`. [↩](#a3)
