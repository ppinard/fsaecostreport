Folder structure
================

To allow the cost report generator to find the different parts, assemblies,
drawings and pictures, these documents must be placed in a particular 
file structure.
Before doing anything, the cost report generator will check that this file
structure exists.

The first thing to do is to create a directory where all the cost report
related documents will be saved.
Something like ``V:\2011\costreport``. 
Keep it simple.
We will refer to this directory as the **base path**. 

Next, for every :ref:`system <systems>`, you need to create a folder in the
base path.
The folder must be named with the two letter abbreviations of the system.
For example, ``BR`` for the *Brake System*.

Then, in each system folder, three folders must be created:

* components
* drawings
* pictures

The following diagram summarised the folder structure:

.. image:: /images/folderstructure.png
   :width: 20%
