Components' structure
=====================

The cost report is composed of 8 systems:

.. _systems:

* A. Brake System (BR)
* B. Engine & Drivetrain (EN)
* C. Frame & Body (FR)
* D. Electronics, Controls & Wiring (EL)
* E. Miscellaneous, Fit & Finish (MS)
* F. Steering System (ST)
* G. Suspension System (SU)
* H. Wheels, Wheels Bearings & Tires (WT)

Each system contains **components**: parts and assemblies. 
There are two types of assemblies, namely:

* system assemblies
* sub-assemblies

System assemblies are high-level assemblies. 
They grouped sub-assemblies together.
An example of a system assembly would be the *Engine* which would group
sub-assemblies such as *Fuel system*, *Intake manifold*, *Cooling system*, etc.
System assemblies are not required for every system in the cost report. 
They are only useful if a process is required to join/install/attach 
sub-assemblies together or to install an assembly on the car. 
See cost reports from previous years for examples.

Sub-assemblies group parts together.
For example, tube A and tube are two parts that need to be welded together to
create the *Exhaust runner*.
The *Exhaust runner* assembly details the welding process.

The following diagram summarises the structure and relations between the
assemblies and parts.

.. image:: /images/structure.png

A few quick pointers:

  * A system assembly is made of sub-assemblies and possibly parts.
  * System assemblies are optional.
  * A sub-assembly is made of parts (no assembly).
  * A sub-assembly does not required to have part.
    It can only contain materials, processes, fasteners and tooling.
  * **IMPORTANT** A part can not be alone in a system. 
    It MUST be incorporated in an assembly. 
  * A part can be part of multiple assemblies.
  * A sub-assemblies can be part of multiple system assemblies.
  
  
These guidelines and restrictions are strictly enforced by the cost report
generator.
The "but it works in my Excel spreadsheet" won't work with the generator!

