pyIsbnScanner
=============

Python project to maintain a Google spreadsheet of all the books I physically own. The pipeline needs some work, but currently one script can read in ISBN numbers from a file, search for that ISBN on Google's Book API and save the metadata to the spreadsheet. Another script can go over this spreadsheet, and populate links to a PDF version as found by an ebook search engine. 

Improvements 
------------

* the list of ISBNs could be populated via webcam (this is not done, but was the intended purpose of scan.py)
* another script to sync the links to PDFs with a local directory, so one can maintain an ebook version of your physical book collection. i
* another improvement would be alternate ways to search for POFs, as still too many cannot be found.
