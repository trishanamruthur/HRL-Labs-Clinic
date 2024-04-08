# Getting Started

```{note}
_More extensive documentation on these topics is available on the [Jupyter Book website](https://jupyterbook.org/en/stable/basics/organize.html)._
```

This page will be a brief overview of how one can navigate, edit, and modify the Jupyter Book documentation that you are reading right now.

## Adding / Editing Pages

(documentation:file-organization)=
### File Organization

Maintaining the organization of files in this repository will be crucial as users continue to build upon this documentation. Following the guidelines laid out here will make it easier for future users to follow, edit, and add upon your contributions to this repository.

Within the root Github/Gitlab repository, the `HRL_book` directory contains all of the source code for building this Jupyter Book. Each **topic** covered in the documentation should be given its own directory within `HRL_book` with a descriptive name pertaining to the that it covers (for example, the information pertaining to charge stability in quantum dots can be found in `HRL_book/charge-stability/`).

Each **topic** should contain a file `cover.md` (or `cover.ipynb`) which will be the launching page for that topic, along with many directories for each **chapter** within the topic. Some of these chapter directories may just contain a single markdown file, while other chapters may rely on many subsections, videos, images, or other content which will all be found within the chapter directory. For ease of navigation, each chapter directory should begin with a number such as `1-` or `2-` indicating its placement within the overall topic. This way, the directory order will match the order of the chapters within the book.

All together, the file structure for this jupyter book should look something like what is shown below.
```
<root repository directory>
├───HRL_book
│   ├───charge-stability
│   │   ├───1-load-unload
│   │   │   ├───loading-and-unloading.ipynb
│   │   │   ├───tunneling.ipynb
│   │   │   ├───img.jpeg
│   │   │   └───video.mp4
│   │   ├───2-sensing-dot
│   │   │   └─── ...
│   │   ├───3-double-dot
│   │   │   └─── ...
│   │   ├───4-qd-arrays
│   │   │   └─── ...
│   │   ├───5-quiz
│   │   │   └─── ...
│   │   ├───6-gloss
│   │   │   └─── ...
│   │   └───7-paper-summary
│   │       └─── ...
│   ├───[other chapters...]
│   ├───files
│   └───PDFs
├───[other topics...]
├───_config.yml
├───_toc.yml
├───references.bib
└───requirements.txt
```
Note that the `tunneling.ipynb` page is a sub-section within the loading/unloading chapter but appears alongside the main page for the chapter, `loading-and-unloading.ipynb`. Also notice that all pages within the chapter (main pages and subsections) get descriptive names so that you can quickly tell which files you are working on instead of having a bunch of files all named `main.md`. Following the conventions here while creating and editing the contents of this Jupyter Book will be critical in maintaining the utility of this tool, so please do it!

### Creating Pages

To create a new page, you first have to create the file corresponding to the page, following the convention detailed in the [section above](documentation:file-organization).

```{tip}
Markdown files (`.md`) should be used for pages which don't rely on code execution, while Jupyter Notebooks (`.ipynb`) can be used when you wish to show runnable code or its output.
```

Once the page content has been created, the page needs to be added to the book,which means adding it to the table of contents in `HRL_book/_toc.yml`. It is relatively straight forward to add/edit this file, but [more detailed instructions can be found here](https://jupyterbook.org/en/stable/structure/toc.html).

Once the page is added to the table of contents, you must re-build the book to see the new page appear. In order to prompt Jupyter Book to look for new pages you should either delete the `_build` directory or run `jupyter-book build --all HRL_book` from the root repository directory.

## Text Content

There is a wide variety of options for displaying text content within a Jupyter Book. More documentation can be found on the [Jupyter Book website](https://jupyterbook.org/en/stable/content/index.html), but the broad strokes will be given here.

### Directive Boxes

Directive boxes are very useful for helping users navigate lots of content. Basic boxes like tips and notes are easy to create:

````
```{note}
This is a note!
```
````
Renders as
```{note}
This is a note!
```

Other basic boxes include `{info}`, `{warning}`, `{tip}`, `{important}`, and many others (see Jupyter Book and MyST documentation). You can also create custom titles for these boxes by using the general `{admonition}` directive. For example,
````
```{admonition} Here is a Custom Directive
:class: tip # this changes the icon/color
Here is where content goes.
```
````
Renders as
```{admonition} Here is a Custom Directive
:class: tip # this changes the icon/color
Here is where content goes.
```

You may also want to have collapsible content on the page for notes that the user may choose to read or not. This can be done with the `{dropdown}` directive, or by adding `:class: dropdown` to an existing directive. For example
````
```{tip}
:class: dropdown
This is a collapsible tip!
```
````
Renders as
```{tip}
:class: dropdown
This is a collapsible tip!
```

```{margin}
This is a margin note! How cool is that.
```
You can also add notes on the margins of the page using the `{margin}` directive. The code 
````
```{margin}
This is a margin note! How cool is that.
```
````
is rendered on the margin next to this paragraph. It is also possible to next directives by adding extra \`s to the outermost directives. 
````{margin}
This is a margin note.
```{note}
And here is a note in the margin!
```
````
For instance, a margin note that contains a note directive would look like this
`````
````{margin}
This is a margin note.
```{note}
And here is a note in the margin!
```
````
`````
A render of this is shown in the margin here as well.

### Equations

Jupyter Book allows for easy embedding of $\LaTeX$ equations within pages. It does this using [MathJax](https://docs.mathjax.org/en/latest/). For inline equations, you can use dollar signs just as you would in a LaTeX document: `$<math goes here>$`. This looks like $a=\frac{b}{c}$. For standalone equations you should use `{math}` directives, for instance
````
```{math}
-\frac{\hbar^2}{2m}\nabla^2\ket{\psi} + V\ket{\psi} = i\hbar\frac{\partial}{\partial t}\ket{\psi}
```
````
will render as
```{math}
-\frac{\hbar^2}{2m}\nabla^2\ket{\psi} + V\ket{\psi} = i\hbar\frac{\partial}{\partial t}\ket{\psi}
```

Jupyter book does have ways of implementing LaTeX-style math (with align blocks and such) however implementing this causes problems with the parsing of other elements in our book, and since the content we have is not _extremely_ math heavy, we have decided to settle for these math directives for now.

Note that you can add numbers to equations by adding the `:label:` tag within the math directive, for instance
````
```{math}
:label: example_label
F(\vec{r}) = -\nabla U(\vec{r})
```
````
will render as
```{math}
:label: example_label
F(\vec{r}) = -\nabla U(\vec{r})
```
and this label can be referenced later on using ``` {eq}`example_label` ```, which renders as {eq}`example_label`.

You can create new commands in markdown cells in jupyter notebooks as follows: 
```
$\newcommand{\span}{\text{span}}$

We denote by $\span(u, v)$ the span of two vectors $u$ and $v$.
```
When rendered, the `newcommand' line is not shown. 

In markdown, we can write
````
```{math}
\newcommand{\span}{\text{span}}
\span(u, v)
```
````
which will render as 
```{math}
\newcommand{\span}{\text{span}}
\span(u, v)
```

### Labels and References

Labels and references are incredibly helpful for allowing users to jump around within the content of this book. Labeling of equations is shown above, but for every other text element markdown labels should be used _preceding the element being labeled_. For instance
````
(getting-started:example-label-2)=
```{tip}
:class: dropdown
This is a labeled dropdown!
```
````
Will render as

(getting-started:example-label-2)=
```{tip}
:class: dropdown
This is a labeled dropdown!
```
And can later be referred to using normal markdown hyperlink syntax ``` [like this](getting-started:example-label-2) ``` which renders [like this](getting-started:example-label-2).

The same can be done with headers, sections, paragraphs, or virtually any text element. For instance the file organization header at the top of this page appears in markdown as
```
(documentation:file-organization)=
### File Organization
```
So that a [hyperlink](documentation:file-organization) can be created later on (using the typical syntax: `[hyperlink](documentation:file-organization)`) that jumps users back to that header.

### Code Style 
To maintain code style for the files, this book uses a Ruff Linter. To check that all the files abide with Ruff's code style you can run 
```
ruff check
```
To check a single file, like test.ipynb, simply run 
``` 
ruff check test.ipynb
```

If you would like to change the specifications of the ruff linter, please see the [official documentation](https://docs.astral.sh/ruff/linter/#ruff-check). The configuration file for our ruff linter is called "ruff.toml." 