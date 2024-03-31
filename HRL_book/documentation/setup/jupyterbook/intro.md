(jupyter-book-setup)=
# Jupyter Book Setup

Instructions for installing and using Jupyter Book. See https://jupyterbook.org/en/stable/intro.html for Jupyter Book's official documentation.

## Installation

Open a terminal. Install Jupyter Book with 

    pip install -U jupyter-book
or

    conda install -c conda-forge jupyter-book

Check installation with

    jb --version
(```jb``` is an alias for ```jupyter-book```, and they can be used interchangeably in the terminal.)

## Building a Book

To generate the html for a site, use

    jb build <dir>

where \<dir\> is the root directory containing all of the book's files (one way to recognize this folder is that it will contain _config.yml and _toc.yml file, provided they haven't been manually moved (don't manually move them)). Note that this might not be the same as the root directory of the git repository. The html will be stored in ```<dir>/_build/html```.

Depending on configuration options, Jupyter Book may cache some results and not re-execute them every time. In particular, many warnings only appear the first time the build command is run. In order to force rebuilding of all files, use the ```--all``` flag. If this still doesn't seem to work, run

    jb clean -a

to remove the _build directory entirely, and then build again.

# Building with Github Actions

This repository uses the workflow at ```.github/workflows/build-site.yml``` to automatically update the Github Pages site with the HRL_book Jupyter Book whenever changes are pushed to the main branch. 

# Building with Gitlab CI/CD
Gitlab CI/CD is a different animal, and we cannot seem to get Gitlab Pages to work enough to test it. But, we've heard you've got this working anyway (3/28/24). 

## Javascript dependencies
While not technically required to build the book, probably these will be accounted for in the CI/CD step. Currently, we get most of our JavaScript packages from CDNs, which will not be available without internet access. Currently, the only package with widespread use on our site is MathJax, which parses the LaTeX in markdown files and Notebook cells. Bokeh (our main Python graphing package) uses Javascript for interactive graphs, but it comes as part of the python package installation rather than a CDN.

MathJax, and any other necessary JavaScript packages, must be accessible to your server so that it can display LaTeX properly. Presumably it can be installed
into a src directory or something, beside the public directory where the html files are stored for Gitlab Pages? You can either clone the MathJax Github repository with ```git clone https://github.com/mathjax/MathJax.git```(all you need to keep is the es5 folder), or you can install npm and use that to install MathJax. See https://docs.mathjax.org/en/latest/web/hosting.html for more detailed instructions.

Wherever you install your Javascript packages, make sure you update ```_config.yml```'s ```html_js_files``` to the correct file paths.