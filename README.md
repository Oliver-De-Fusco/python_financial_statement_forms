# Required imports

pypdf - Most recent version (3.10)

# File structure

In the default state of the program : 

- (File)
  - `pdf_object_sort_2.py`
  - `pdf_reader.py`
  - all the pdf's you wish to rename

`pdf_object_sort_2.py` can be modified to take the locations of the pdf's from other locations by changing the inital assignment of the variable `report_list`, however `pdf_reader.py` will need to be in the same location as `pdf_object_sort_2.py`.

# pdf_object_sort_2.py

__Run this file to rename the pdf files.__

`pdf_object_sort_2.py` uses `pdf_reader.py` to rename the files and generates the expected sequence of the files, this also handles duplicates by renaming them with `"Duplicate - {name}"` but can be modified to move them to another file

If the program has trouble with the company name it should be set manually by adding `company={manually set name}` when creating the list of pdfs to modify.

# pdf_reader.py

Responsible for reading the contents of a pdf file and provides a class for easier data handling.

__This requires the libary pypdf.__

# randomise_names.py

Used for testing purposes but recomened to use if you need to run `pdf_object_sort_2.py` more than once on the same files. This is because the program will add "Duplicate - " to the start of the file name continuously and will lead to very long names otherwise.

Placed in the same directory as the pdfs to be renamed
