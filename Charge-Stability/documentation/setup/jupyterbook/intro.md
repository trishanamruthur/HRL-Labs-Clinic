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