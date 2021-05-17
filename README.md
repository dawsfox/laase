## Usage of laase.py

### Installation and Dependencies

`laase.py` was written for Python 3.8.2. It imports four modules: `os`, `glob`,
`pdftotext`, `re` (regular expression), and `math`. The `pdftotext` module
depends on `poppler` which must be installed prior to installing the module.
Installation of the modules was performed with `pip`.

### Usage

`laase.py` is currently a command line tool. It should be run using the
`python3` binary. It does not except any arguments.

Upon running the file, a list of numbered options will be presented. They are
listed from first to last in the order a user should select them to run
correctly. Option 1 is to set the path of the directory holding the `.pdf`
files to be indexed for searching. The path can be absolute or relevant. Option
2 will give the user the ability to add search categories and shows the format
in which they should be entered (category first, then relevant category terms).
Option 3 is to build the index; this must be selected before entering a search
query and after setting the directory of the local `.pdf` collection.

Please note that if an error is encountered while building the index, there are
two commonly noted causes: that the path entered for the `.pdf` collection is
not valid or does not contain any readable `.pdf` files or that one of the
`.pdf` files has a format that is incompatible with the `pdftotext` module. I
have only encountered the latter once, and it occurred on a `.pdf` file that
appeared to be from the 1980's, so this should not be a common error. There is
no current workaround other then removing the document from the indexing
directory.

Option 4 is to print the index. This is only used for debugging or if the user
is curious. It prints a large amount of index information, so users be warned.
Option 5 will ask you to enter a query for searching. After entering the query
(which should avoid symbols and should be space separated words for best
results), the results will appear. At the moment, the code retrieves 5
documents deemed to be relevant. This number can be changed by modifying the
argument passed to the `retrieve` function. The tuning parameter for the
pivoted normalization ranking method can also be changed by editing the value
of the `b` global variable in the code (by default it is `0.2`). The results
will also show a categorization for each search category added by the user.

The search directory, search categories, and index are not persisten, so they
must be set/built each time the execution terminates.
