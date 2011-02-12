Drawings
========

Drawings should be saved in the ``drawings`` folder of their corresponding 
system.
Only PDF drawings are accepted.
If you have a JPG drawing (e.g. for a wiring diagram), it needs to be converted
to a PDF.

The cost report generator does not understand multi-pages PDF files containing
several drawings.
Every drawing should have its separate PDF file.
This file should be named after the full part number of that part or assembly.
For example, the drawing for the part ``BR-00001-AA`` should be 
``BR-00001-AA.pdf`` and should be located in the ``BR/drawings`` folder.

If the drawing of a part or an assembly has more than one page, a suffix
must be added to the name of the file.
For example, the assembly ``BR-A0001-AA`` has a two page drawing.
The PDF file for the first page should be ``BR-A0001-AA-00.pdf`` and the
second page ``BR-A00001-AA-01.pdf``.
Use Adobe Acrobat to export multi-pages PDFs to single-page PDFs.

.. note::

   The suffix can be anything as long as when the files are alphabetically
   ordered the first page is the first file and the last page the last file.

