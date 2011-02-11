Let's make a part
=================

*More precisely, "Let's compile the materials, processes, fasteners, tooling 
costs to make a part" or "Let's take the fun out a real part and convert it
into tons of numbers"!* 

A part is costed by listing its different:

* materials (raw material, purchase components, etc.)
* processes (machining, cutting, riveting, wrenching, assembling, etc.)
* fasteners (bolts, nuts, straps, etc.)
* tooling (welding, oven, casting, etc.)

The SAE provides exhaustive tables of different materials, processes, fasteners 
and tooling. 
A part should only be made out of those. 
If something is missing in the tables, a "Add Item Request" must be submitted 
(see `FSAE Online <http://fsaeonline.com/eAIR.htm>`_). 

The Excel spreadsheet aims to standardise and simplify the process of making
a part for the cost report. 
All the SAE tables are incorporated and their items can be accessed quickly
by using their ID. 
Some of the columns gets automatically filled or gives hints to the user how
to fill them. 
However, it is important to always double check in the actual SAE tables to 
make sure the automatically filled cells are correct. 
More example about that below.

.. contents::
   :local:

Overview of the spreadsheet
---------------------------

The Excel spreadsheet template contains 8 sheets:

* **TM-A0001-AA**: Template for assemblies
* **TM-00001-AA**: Template for parts
* **tblMaterials**: SAE table for materials
* **tblMaterialsCrossReference**: Help on how to cost some parts
* **tblProcesses**: SAE table for processes
* **tblProcessMultipliers**: SAE table for process multipliers
* **tblFasteners**: SAE table for fasteners
* **tblTooling**: SAE table for tooling

In short, the sheets of SAE tables starts with ``tbl`` and should never be
modified or renamed.
They can however be filtered using the auto filter (little arrow in the
header of the columns).

The two template (for part and assembly) are the sheets that could be COPIED
and filled out.
Note that only specific cells need to be modified in the template and 
additional rows can only be inserted at specific places.
You should never have to add a column.

Part template
-------------

After copying the part template, the first thing should be to renamed the 
sheet with the complete part number (e.g. ``BR-00001-AA``).
The part template is made out of 5 sections:

* Header
* Materials table
* Processes table
* Fasteners table
* Tooling table

Header
^^^^^^

The header gives the details about the part.
The important information to be modified are:

* The part's name (labelled ``Part``)
* The part's base part number. 
  This is the ``00001`` in ``BR-00001-AA``.
  
  **IMPORTANT** If you type ``00001`` in the cell, Excel will think it's the 
  number ``1``. You MUST type ``'00001`` (apostrophe, zero, zero, zero, 
  zero, one).
  
* The part's suffix (in other words the revision)
* (Optional) Details about the part (a short description if the name is not
  self-explanatory)

The other information in the header (university, system, assembly, car#, 
quantity, assembly cost, extended cost) will automatically be calculated by the
cost report generator. 
They can be left blank or to whatever values they are in the template.

Materials table
^^^^^^^^^^^^^^^

A material can either be a bought finished product (e.g. an engine block) or
raw material. 
Careful, a bolt, a rivet, etc. are not materials but fasteners.

Let's take the example of making a steel tube (as it's a very common part).
In the materials table (``tblMaterials``), the item *752* is for 
*Steel, Mild* which would correspond to a 1020 steel grade.
In the first column, type ``752``. 
The row should know look like this:

.. image:: materials1.png

The name of the materials and its unit cost per kg are automatically filled
out using the ``VLOOKUP`` function of Excel.
Since tubes are cost by their mass, we should write a use/description of 
the tube characteristics (e.g. round tube, 1" OD, 0.065” thick., 10" long).
Now, we need to calculate the mass of such tube, well its volume times the
density of steel 7.8 g/cm3. 
This should be done on a piece of paper or a separate spreadsheet.
For this particular tube, the mass is 0.126 kg.
