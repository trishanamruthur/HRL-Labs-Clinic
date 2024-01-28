# HRL-Labs-Clinic
A sample educational Jupyter book covering charge measurement and stability in quantum dot arrays.

## Setup
### Jupyter Book
Instructions for installing and using Jupyter Book. See https://jupyterbook.org/en/stable/intro.html for Jupyter Book's official documentation.
#### Installation
Open a terminal. Install Jupyter Book with 

    pip install -U jupyter-book
or

    conda install -c conda-forge jupyter-book

Check installation with

    jb --version
(```jb``` is an alias for ```jupyter-book```, and they can be used interchangeably in the terminal.)

#### Building a Book

To generate the html for a site, use

    jb build <dir>

where \<dir\> is the root directory containing all of the book's files (one way to recognize this folder is that it will contain _config.yml and _toc.yml file, provided they haven't been manually moved (don't manually move them)). Note that this might not be the same as the root directory of the git repository. The html will be stored in ```<dir>/_build/html```.

Depending on configuration options, Jupyter Book may cache some results and not re-execute them every time. In particular, many warnings only appear the first time the build command is run. In order to force rebuilding of all files, use the ```--all``` flag. If this still doesn't seem to work, run

    jb clean -a

to remove the _build directory entirely, and then build again.

#### Building with Github Actions

This repository uses the workflow at ```.github/workflows/build-site.yml``` to automatically update the Github Pages site with the Charge-Stability Jupyter Book whenever changes are pushed to the main branch. (It relies on some public Github workflows, so it probably won't translate directly to Gitlab. Gitlab Pages is tricky to set up so we haven't managed to test that yet.) See https://jupyterbook.org/en/stable/publish/gh-pages.html for more info. Note that the repository settings must give Actions (or at least this particular one) permission to push to the gh-pages branch. 


### Building Notebook Locally
Clone this repository after Jupyter Book is set up.

Run the following in the terminal
```
jupyter-book build --all Charge-Stability
```
Copy given url to a browser to view Notebook locally.
Once notebook is built, further instructions for features can be found in Documentation/Tutorials section of site.

Note: the --all recompiles the pages, so don't need to build folder when recompiling
