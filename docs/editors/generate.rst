Generate the report
===================

The Excel spreadsheets were converted to CSVs, the drawings are all there and
properly renamed to their respective part number, the pictures have proper 
filenames and they were resized, the extra files are all there, well then you
are ready to generate the cost report!
Generating the cost report is a 2 step process with an optional third one.
Let's look at the optional one first.

Error checking
--------------

When generating the cost report, the generator will always check for errors.
However, instead of generating the whole cost report every time you want to
check for errors, the cost report generator allows you to only check for errors
in one or many systems without generating the actual report.
The advantage of this is that you can process one system at the time and fix 
the errors.
Once a system has no more errors, you can mark it off and move to the next one.

How to do this?

* Open a command prompt and change directory to the cost report base path.
* Type the following command to check the *Brake system*::

   costreport-app -r BR
   
  or to check the *Engine and Drivetrain System*::
  
   costreport-app -r EN
  
  or to check the *Brake System* and *Engine and Drivetrain System*::
  
   costreport-app -r BR EN
  
  etc.
  
* The program stops when one error is detected. 
  To understand the error, look at the last line printed in the command 
  prompt.
  Apart from the programming giberish, there is a short explanation of the 
  error.
  If this description is not enough, report a :ref:`bug <bug>` with the whole error 
  message.
  
Generating the LaTeX document
-----------------------------

After you are done checking for errors (or you decide to skip that step), it is
now time to generate the LaTeX document.
If you did everything right before, this is the easiest step in the world.

* Open a command line prompt, change directory to the cost report base path
  and type::
  
   costreport-app -w
   
* After a few seconds and a lot of things getting printed in the command line
  prompt, a text file named ``costreportXXXX.tex``will be generated in the
  cost report base path (the ``XXXX`` are replaced by the year).
* Do not move this file, it's fine where it is. Move to the next step.

Generating a PDF
----------------

This is the moment of truth.
We need to generate the PDF out of the LaTeX document.

* Open a command line prompt, change directory to the cost report base path
  and type (replace the ``XXXX`` by the year)::
  
   pdflatex costreportXXX.tex
  
* It will probably take a minute or so for the PDF to be produced if no error
  occurs.

Errors
^^^^^^
If an error occurs, the program won't terminate. You will get a ``?``.
Press Ctrl + C to terminate the program. Here it's not your fault if you get
an error. Therefore, immediately report a :ref:`bug <bug>` with the whole error 
message in it.

Warnings
^^^^^^^^

Ok you don't get errors, but you get some ``LaTeX Warning``'s printed after
the program exits. 
They will most likely look like this::

   LaTeX Warning: There were undefined references.
   LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.

Don't panic, these are normal. 
You might have to rerun the program once or twice to get rid of them.
To make the cross-reference (links between pages), LaTeX needs to know what
the references are first (first pass).

If some of the warnings do not disappear, report a :ref:`bug <bug>`.

Final check
^^^^^^^^^^^

If there was no errors and no warnings, you are pretty sure that the PDF is 
properly formatted. Quickly go over to make sure everything is alright.

