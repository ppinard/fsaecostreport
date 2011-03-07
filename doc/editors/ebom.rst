Electronic BOM (eBOM)
=====================

The electronic BOM is an Excel spreadsheet that should be submitted on a CD
with the printed copy of cost report.
The template of the eBOM can be found on the `FSAE online <http://fsaeonline.com/>`_
website.
It is basically a summary of all the BOM found at the beginning of each system
in the cost report.

Instead of having to manually re-enter all the parts and numbers in the eBOM,
the cost report generator automatically creates a CSV file that contains all
these information.
The CSV file can be imported in Excel and reformatted to match the colors,
fonts and border lines of the original BOM.
The links in the ``Cost Summary`` sheet must also be updated.

The eBOM must be generated after the cost report has been created AND compiled
to a PDF.
The eBOM needs the page numbers of the different cost tables and this 
information is only accessible after the PDF is generated.

So after the PDF is generated,

* Open a command line prompt, change directory to the cost report base path
  and type::
  
   costreport-app --ebom
   
A CSV file will be created in the base path.
