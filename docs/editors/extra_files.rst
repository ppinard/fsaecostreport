Extra files
===========

A few extra files are required to be present in the cost report base path in
order to generate the cost report.

* carnumber.txt
* teamname.txt
* university.txt
* year.txt
* logo.jpg
* introduction.txt

The ``carnumber.txt`` is a one-line text file with the number of the car as 
registered in the competition.
The ``teamname.txt`` is a one-line text file with the name of the team, 
in occurrence ``McGill Racing Team``.
The ``university.txt`` is a one-line text file with the university's full name, 
in occurrence ``McGill University``.
The ``year.txt`` is a one-line text file with the current year. 

The ``logo.jpg`` should be the logo of the team. 
It will be displayed in the header of every page.
It will automatically be scaled to fit the header, but an image of about 
5 mm (~50 pixels) high would be a good size.
Note that the logo must be a JPG.

The ``introduction.txt`` is a text file with the text for the introduction 
page of the cost report
The introduction should fit on one page once in the cost report, therefore
it should have between 400 and 500 words.
The introduction will be interpreted as a LaTeX document.
Refer to the `LaTeX syntax <http://en.wikipedia.org/wiki/Wikibooks:LaTeX>`_ 
if you want special formatting (bold, italic, item lists, etc.)

