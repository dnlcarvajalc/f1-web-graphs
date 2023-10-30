# f1-web-graphs
This README will guide you through the process of creating a Conda environment and setting up a Git hook to ensure PEP 8 compliance using Black.

## Getting Started

### Prerequisites

Before you begin, make sure you have the following installed:

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

---
### Clone the Repository

```bash
git clone git@github.com:<your_username>/f1-web-graphs.git
cd f1-web-graphs
```
---
### Create conda environment

```
conda create --name f1_web python=3.10
```
### Activate the environment
```
conda activate f1_web
```
### Install dependencies
```
pip install -r requirements.txt
```
---
### Git hook for black

I recommend to create a git hook in order to make easier the use of pep8 during the project. For this reason you need to create a file in .git/hooks/pre-commit <== this file will contain the next code:

```
#!/bin/bash

# Ensure Black is installed
if ! command -v black &> /dev/null
then
    echo "Black is not installed. Please install it using 'pip install black'."
    exit 1
fi

# Run Black to format staged Python files
git diff --staged --name-only --diff-filter=ACM -- '*.py' | xargs black

# Add the formatted files to the staging area
git add .

# Continue with the commit
exit 0
```

and in the repo folder you can create a file called "pyproject.toml" with the following code:

```
[tool.black]
line-length = 100
include = '\.pyi?$'
exclude = '''(
    /(
        \.eggs/
      | \.git/
      | \.hg/
      | \.mypy_cache/
      | \.tox/
      | \.venv/
      | _build/
      | buck-out/
      | build/
      | dist/
    )/
  | ^setup\.py$
)'''
```
### To use pytest to see coverage of unit testing:
```
pytest --cov=src
```
```
coverage html
```