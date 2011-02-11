What does the generator do?
===========================

The main idea behind the generator is to facilitate the gigantic formatting 
and editing task of combining every single assembly and part of the car into
one binder. 
The generator takes the cost tables, drawings and pictures, double checked 
their values and organised them into a final report, ready to be submitted to
the SAE. 

This whole process can be split into six parts, which are graphically
represented in the following figure:

#. filling cost tables for assemblies and parts in *Excel* using the 
   tables provided by the SAE
#. generating high quality drawings with *ProE* for each part and assembly
#. taking pictures of the different parts and assemblies
#. exporting the Excel data to comma separated value (CSV) files
#. running the generator to create a 
   `LaTeX <http://en.wikipedia.org/wiki/LaTeX>`_ file
#. compiling the *LaTeX* file into a PDF

.. image:: /images/generator.png
   :width: 70%

The generator comes in at the 4th and 5th step.
It converts well organised CSVs, drawings and pictures into a LaTeX document, 
ready to be compiled to a PDF.

The users are in charge of step 1 to 3. 
They therefore do not have to use the generator per say. 
However, a basic understanding of what the generator is important to know
how to fill the cost tables, number the parts, label the drawings, etc.

The editors perform quality control on step 1 to 3 and executes the other 
three steps.
The generator will most likely point out a series of errors that need to be
fixed in order to generate the LaTeX document.

What the generator is not?
--------------------------

* A bug free program
* An automatic generator of cost tables
* A cost judge (no quality assessment: garbage in, garbage out)
