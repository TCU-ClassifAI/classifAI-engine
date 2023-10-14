# Instructions for pre-commit


## Installation
In the root directory of the project, run the following commands:
```bash
pip install -r backend/requirements.txt -r backend/requirements-dev.txt 

pre-commit install
```


## Usage
`pre-commit run --all-files` to run all hooks on all files.

Just commit as usual. The pre-commit hook will run automatically.

REMINDER: You have to re-run `git add` after the pre-commit hook runs. 

## Adding a new hook
To add a new hook, add a new entry to `.pre-commit-config.yaml`.

Then run `pre-commit install` to install the hook.

