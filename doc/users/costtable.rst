.. _costtable:

Let's make a part
=================

.. epigraph::

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

.. note::

   The latest version of the master template can be found in the Downloads 
   section of https://launchpad.net/fsaecostreport.
   

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

After copying the part template, the first thing should be to rename the 
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
  
.. warning::
  
   If you type ``00001`` in the cell, Excel will think it's the 
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

.. image:: /images/materials1.png

The name of the materials and its unit cost per kg are automatically filled
out using the ``VLOOKUP`` function of Excel.
Since tubes are cost by their mass, we should write a use/description of 
the tube characteristics (e.g. round tube, 1" OD, 0.065” thick., 10" long).
Now, we need to calculate the mass of such tube, well its volume times the
density of steel 7.8 g/cm3. 
This should be done on a piece of paper, a separate spreadsheet or 
in your head.
For this particular tube, the mass is 0.126 kg.

Where should this value be entered?
Strangely, in two cells: under the column ``Size1`` and under ``Quantity``.
Why?
Because the "size" of this material is 0.126 kg. 
So it should be under ``Size1`` as the units of ``Size1`` are kg.
The odd one is the quantity.
The subtotal of a row is always (check the Excel formula):

  subtotal = unitcost * quantity
  
So why don't we change this formula?
It makes things a lot simpler if the formula is the same for all items.

.. note::

   In fact, the subtotal value in the Excel spreadsheets is completely
   ignored by the cost report generator.
   The generator calculates its own subtotal from the unitcost and quantity
   values.
   So, even if you replace the formula and put $6 trillions as the
   subtotal of a material, the subtotal that will appear in the cost report
   will be unitcost * quantity of that material.
   
So what if I have two tubes with the same dimensions? What is the quantity?
Well you are doing some wrong: each tube should be a part and you should make 
an assembly to group them together.

Your final row should look like this:

.. image:: /images/materials2.png

Another possibility you will get when selecting a material is that the 
unitcost of an item will be a formula (e.g. ``[C1]*[Size1]^2+[C2]``) instead 
of a value.

.. image:: /images/materials3.png

You need to replace the ``[C1]``, ``[Size1]`` and ``[C2]`` by the actual 
values.
The ``[C1]`` and ``[C2]`` values can be found in the SAE tables (they are
constants).
For ``[Size1]``, it should refer to the value in the ``Size1`` column.
For a description of what the value of ``Size1`` means in the equation, 
refer to the comments column of the SAE tables.
The units of ``Size1`` are given in the column ``Unit1``.

.. image:: /images/materials4.png


Processes table
^^^^^^^^^^^^^^^

A process is anything performed on the materials and fasteners: machining, 
drilling, assembling, torquing, screwing, etc.
Think of every steps you need to do to make or assemble a part as small and
insignificant it might be.
It is very easy to loose points because someone forgot a 
``Assemble, 1 kg, Line-on-Line`` in his processes.

.. note::

   Remember the cost tables (processes table and others) should refer to 
   how you would make a part or assemble parts if you were producing 1000 
   MRTs per year.
   It does NOT have to reflect the actual process that you use in reality
   to make it.
   For example, you probably used a ratchet to screw the nut on the bolt.
   In a production scenario you would probably use a power tool for that 
   (if the bolt is easily accessible).

All the instructions given for the Materials table are valid for the 
processes table even if some of the columns are different.
The major difference for the processes table is the process multiplier.
As you can imagine, machining steel is a lot easier than to machine titanium.
The SAE cost table specifies only one cost for machining, but requires you, 
for certain processes, to multiply this cost by a process multiplier. 
The column ``Multiplier Type Used`` in the ``tblProcesses`` table is there for
that.
The value for the process multipliers can be found in the 
``tblProcessMultipliers`` sheet.

As such, if you select the process 127 - Machining, a question mark will appear
in the ``Multiplier ID`` column, telling you that a process multiplier must be
specified.

.. image:: /images/processes1.png

Enter the ID of the process multiplier and the value will appear in the next
column.
Always enter the ID of the process multiplier even if its value is 1.
The cost judges needs to see that.

.. image:: /images/processes2.png

.. warning::

   Also note that in the SAE processes table, there is a column 
   ``Tooling Required``. 
   This column tells you if you need a tooling for this operation. 
   Careful, there is no question mark or notice that is given to you about this.
   You need to remember to add the proper item in the tooling table.
   
.. note::

   The subtotal of a process item is always, and always should be, the unitcost
   times the quantity times (if specified) the process multiplier.

Fasteners table
^^^^^^^^^^^^^^^

A fastener is to attach materials or parts together.
The table and the instructions are exactly the same as for the materials table.

Tooling table
^^^^^^^^^^^^^

Most tools and equipment used to build and assemble the parts of the car are
not considered in the cost report (perhaps included in the item cost?...).
The tooling table refers to tools that "are specific to the part geometry".
The SAE rule book gives the example of a casting die.
The die is a tooling but the actual press to stamp a part out of the die is not.

The ``PVF`` columns stands for "Production Volume Factor".
In other words, how many cars can be produced with this tooling?
The default value is 3,000 for 3 years of producing 1,000 cars.
It could be less, for example, the tub for a carbon monocoque.

.. note::

   The subtotal of a tooling item is always, and always should be, the unitcost
   times the quantity divided by the PVF.

In summary
----------

.. _costtable_do_dont:

A few important do and don't:

* Always use the IDs
* You should never have to erase a formula. 
  The only exception is for the unit cost that are made of an equation which 
  you should replace with the correct formula.
* Never changed the subtotal formula.
* There should NOT be empty rows in the tables.
* If you need extra rows in a table, insert a new row and copy the content
  of an empty row to get the correct formulas.
* Never change the formatting of the cells.
  I know it's weird to have a subtotal as 1.2543253 instead of $1.25, but
  all the values should be numbers with no dollar sign.
  The dollar sign and the proper rounding are done by the generator. 
* Remember the cost tables should refer to how you would make a part or 
  assemble parts if you were producing 1000 MRTs per year.
  It does NOT have to reflect the actual process that you use in reality
  to make it.