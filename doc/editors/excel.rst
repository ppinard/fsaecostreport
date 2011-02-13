Excel to CSVs
=============

Once the users have submitted to the editors their Excel spreadsheet, the first
thing to do is to check every single one of them to make sure:

* the header is correctly filled
* the sheet are labelled after the full part number of a part or assembly
* there is no missing part
* the information entered in the cost table is correct

  * enough description in the *Use* column
  * no $ sign
  * and all other :ref:`do and don't giving <costtable_do_dont>` at the end 
    of the :ref:`Let's make a part <costtable>` documentation page.
    
Next, the Excel files (XLS or XLSX) must be placed in the proper system 
folder in the cost report base path.
For instance, the *Brake System* spreadsheet (``BR.xlsx``) must be placed in
the ``BR`` folder of the cost report base path.
If two or more people work on a system and have independent spreadsheets, place
all the files in the system's folder.
For example, the file ``EN-engine.xlsx`` and ``EN-drivetrain.xlsx`` can both
be saved in the ``EN`` folder.
They will both be converted to CSV files.

.. warning::

   If the cost table for a part number is present in two Excel spreadsheets, 
   one will overwrite the other WITHOUT warning.
   In other words, different Excel spreadsheets cannot have common
   part numbers.
   One can however refer to a part in another spreadsheet (e.g. in an assembly)

Instead of manually exporting every single sheet in the spreadsheets to CSV, 
there is a macro built-in the cost report generator for that.
The macro allows you to export to CSVs all the spreadsheets or those for a
particular system. 

* Open a command line prompt
* Change directory to the cost report base path
* Type the following to convert all spreadsheets to CSV files::

   costreport-app -x
   
  or to convert only the *Brake System* spreadsheet(s)::
  
   costreport-app -x BR
   
  or to convert the spreadsheets from the *Brake System* and the 
  *Suspension System*::
   
   costreport-app -x BR SU
   
  etc.

The macro opens the spreadsheet, converts every sheet which name is a part
number and saves the CSV in the system ``components`` folder.
After running the macro, double check that the ``components`` folder 
contains CSV files.
If an error occurs during the conversion, report a :ref:`bug <bug>`.
 