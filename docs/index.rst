Welcome to FSAE cost report generator's documentation!
======================================================

The documentation is divided into three sections: 

* Users
* Reviewers/editors
* Developers

A user is someone that will be creating cost tables for one or many systems. 
This part of the documentation is therefore an introduction on what is the cost
report and how to fill out the cost tables to facilitate the task of the 
editors. 
The editors should also understand all the requirements given in this first
section.
The reviewers/editors are those that will be checking the cost tables
created by the user, assembling the drawings and pictures and finally creating
the full cost report. 
This section goes deeper on how the cost report generator works.
Finally, the last section is aimed at future developers of the generator. 
It gives an overview of the API.

Users
-----

.. toctree::
   :maxdepth: 1
   
   users/generator.rst
   users/gettingstarted.rst
   users/component_structure.rst
   users/partnumbering.rst
   users/costtable.rst
   users/costtable2.rst
   users/makebuy.rst
   users/drawings.rst
   
Reviewers/Editors
-----------------

.. toctree::
   :glob:
   
   editors/*
   
Developers
----------

.. toctree::
   :glob:
   
   fsaecostreport/*

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
