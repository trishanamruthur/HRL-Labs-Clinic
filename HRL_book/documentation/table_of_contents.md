# Table of Contents Best Practices
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

```{warning}
You MUST add a title line to the top of each file that is in the table of contents. If not, the page will not show up when you try to build the book.
```

```{warning}
The table of contents is VERY sensitive to spacing issues. Make sure that if you see any errors relating to toctree, check the spacing and ordering of the files you are trying to add. 
```