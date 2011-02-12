Installation
============

.. contents::
   :local:

Requirements
------------

Here are the basic requirements to run the cost report generator.
The explanations regarding the installation of the generator and some of the 
other requirements is given below.

* Windows OS (tested under XP) [#f1]_
* Microsoft Excel [#f1]_
* MikTeX (or equivalent)
* Adobe Acrobat (or equivalent) [#f2]_
* Cost report generator

Before we start
---------------

The cost report generator is a command line based software.
Therefore, a basic knowledge of how the Windows command line works is required.

You can open a command line prompt by pressing the Windows key + R and 
typing ``cmd``.
A reference of the command can be found at http://ss64.com/nt/.
However you will most likely only need the command to change directory 
(``cd``)::

  cd \ 
  cd /D v:
  cd ..
  cd C:\costreport

MikTeX
------

MikTeX is the Windows compiler of LaTeX documents.
In other words, it is the software that converts a LaTeX document into a PDF.
MikTeX can be downloaded from http://miktex.org/.
You can install the basic or complete MikTeX system; it does not matter for
our current application.
The portable version also works if you don't have the administrative 
access to the computer.

Settings up the environment variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is important to have MikTeX in the Windows PATH environment variable.
This allows to call MikTeX program more easily.
   
* Press the Windows Key + R.
* Type ``SYSDM.CPL`` and press Enter.
* Go in *Advanced System Settings*
* Click on *Environment Variables* (at the bottom)
* Under *User variables*, click *New*
* Enter the variable name as ``PATH``
* Enter the variable value as ``{{ PATH_TO_MIKTEX }}\miktex\bin``.
  You need to replace the ``{{ PATH_TO_MIKTEX }}`` by the installation 
  directory of MikTeX (usually ``c:\Program Files\MikTeX 2.9``)
* Press *OK* until all the windows are closed.

First test
^^^^^^^^^^

After the installation, here is how to test that the installation worked.

* Copy the text in the following box in a text editor (i.e. ``notepad``)::
  
    \documentclass[letterpaper]{article}
  
    \begin{document}
    Hello World!
    \end{document}

* Save the file as ``hello.tex`` in a known folder
* Open a command line prompt and ``cd`` to the folder containing the 
  ``hello.tex`` file.
* Type the following command and press Enter::

    pdflatex hello.tex
  
* If everything works, a PDF file (``hello.pdf``) should be created in the 
  folder. 
  Open it, it should say "Hello World!".
  
In short, we created a LaTeX document (our ``hello.tex``) and we compiled it
to a PDF using the program ``pdflatex``.
That's all you need to know for the cost report.

Second test
^^^^^^^^^^^

A second test to go a bit further and prepare MikTeX for the cost report.

* Copy the following text in a text editor and save the file as 
  ``hello2.tex``::

   \documentclass[landscape, letterpaper]{report} 

   \usepackage[top=3cm, bottom=3cm, right=1cm, left=1cm]{geometry}
   \usepackage{graphicx}
   \usepackage{multirow}
   \usepackage{url}
   \usepackage{amsmath}
   \usepackage{longtable}
   \usepackage{titlesec}
   \usepackage{array}
   \usepackage{colortbl}
   \usepackage{multicol}
   \usepackage[final]{pdfpages}
   \usepackage[english]{babel}
   \usepackage[latin1]{inputenc}
   \usepackage[pdftitle={Cost Report}, pdfsubject={Formula SAE Competition Michigan}, pdfauthor={McGill Racing Team}, colorlinks=true, linkcolor=blue, pdfborder=0 0 0, pdfhighlight=/I, pdfpagelabels]{hyperref}
   \usepackage{fancyhdr}
   \usepackage{setspace}

   \begin{document}
   Hello again!
   \end{document}
   
* In the folder where ``hello2.tex`` is saved, type the following command::

    pdflatex hello2.tex
    
* You will most likely be prompted several times (>10) by MikTeX to install 
  specific packages. 
  Accept to install all these packages.
  They are required to compile the cost report.
  
* If everything works, a PDF ``hello2.pdf`` should be created.

Cost report generator
---------------------

The first thing to do is to download the latest version of the cost generator
application on https://launchpad.net/fsaecostreport.
Make sure you always have the latest revision.
Extract the ZIP in a known folder. 

Settings up the environment variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is important to have cost report generator program in the Windows PATH 
environment variable.
The procedure is exactly the same as for MikTeX.

.. note::

   It only needs to be done once if you always unzip the cost report generator
   updates in the same directory.
   
* Press the Windows Key + R.
* Type ``SYSDM.CPL`` and press Enter.
* Go in *Advanced System Settings*
* Click on *Environment Variables* (at the bottom)
* Under *User variables*, select the previously create variable ``PATH``
  and click *Edit*
* At the end of the variable value (do not erase the MikTeX path), enter
  the following ``;{{ PATH_TO_COST_REPORT_GENERATOR }}\bin``.
  Note the semi-colon to separate the MikTeX and cost report generator paths.
  You need to replace the ``{{ PATH_TO_COST_REPORT_GENERATOR }}`` by the 
  folder where you extracted the ZIP.
* Press *OK* until all the windows are closed.

First (and only test)
^^^^^^^^^^^^^^^^^^^^^

To test the cost report generator is very simple. 
We just need to make sure that the program runs.

* Open a command line prompt, type the following command and press Enter::

   costreport-app
   
* You should get a help message that looks similar to this::

   Usage: costreport-app [options]

   Options:
     -h, --help            show this help message and exit
     -b BASEPATH, --basepath=BASEPATH
                           Base path of the cost report (i.e. folder containing
                           the systems) [default=current directory]
     -x, --xlsx2csv        Convert the Excel spreadsheets in CSV files
     -r, --read            Read the CSVs, drawings and pictures and check for
                           errors
     -c, --create          Read, process and write the cost report and e

* Congratulations everything is properly installed!

.. rubric:: Footnotes

.. [#f1] Windows and Microsoft Excel are only required to fill out the cost
         reports and export them to CSV files. After that, any platform
         with Python and LaTeX can technically be used.

.. [#f2] Required to convert a multi-pages PDF into single-page PDFs.
         Other PDF editing software could be used.
