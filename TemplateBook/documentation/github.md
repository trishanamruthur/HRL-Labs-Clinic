# Github Documentation

This documentation is for how to work with the Github repository the clinic team is using for development. The repository is [here](https://github.com/trishanamruthur/HRL-Labs-Clinic). If you would like to edit the repository and do not have access, please email hrl23l@cs.hmc.edu, or talk to Thaddeus Ladd or Paul Jerger.

If you don't have experience with Github, [here](https://docs.github.com/en/get-started/quickstart) is a quick guide.

Our current work (as of 12/8/23) is all being done in the ```HRL_book``` directory of the repository.

## Other Software

You will need [Jupyter Book](jupyter-book-setup) to render any changes you make as html.

The repository has an associated Github Pages site: https://trishanamruthur.github.io/HRL-Labs-Clinic. Currently (1/30/24), this site is built with Github Actions. It can be done manually with ```ghp-import```. This can be installed with ```pip install ghp-import```, and run with ```ghp-import -n -p -f HRL_book/_build/html``` from the repository root to update the site to reflect any changes in the main branch.

The code in our book uses several Python packages, listed in ```HRL_book/requirements.txt```. They can be installed with pip or, in most cases, conda (other than ```jupyterquiz``` and ```jupytercards```, I think).