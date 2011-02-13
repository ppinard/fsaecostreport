Let's make an assembly
======================

.. epigraph::

   *Not another page to read!* 

Well this one is easy, an assembly is costed exactly like a part with two 
exceptions: the header and one more table.
That's why assemblies have a different template than parts.
You should therefore copy the assembly template sheet and modified it.

Header
------

The header is slightly different: there is one less row.
However, that row (``Assembly``) was not important for the part, so it is 
basically the same thing. 
The real difference is that the quantity must be specified for assemblies if
they are top-level assemblies.
A top-level assembly is an assembly that does not have a parent system 
assembly.
So all system assemblies are top-level assemblies, and sub-assemblies that 
do not fall under a system-assembly are also considered top-level.
The quantity must be specified for these types of assemblies because it is 
the only way for the generator to know how many there are, their quantity
cannot be back-calculated.

Parts table
-----------

The parts table list the parts that are part of an assembly!
The first column ``PN`` should be the complete part number of the part
(e.g. ``BR-00001-AA``).
You can use references for the name and part cost.
The quantity field is important as it is used by the generator to count the
number of occurrences of a part.
Again, the subtotal is automatically calculated by the generator.
It should always be the part cost times the quantity.

