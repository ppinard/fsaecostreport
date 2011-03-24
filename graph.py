#!/usr/bin/env python
"""
================================================================================
:mod:`graph` -- 
================================================================================

.. module:: graph
   :synopsis: 

.. inheritance-diagram:: graph

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os

# Third party modules.
from pylab import * #@UnusedWildImport

# Local modules.

# Globals and constants variables.

def cost_summary(basepath, systems):
    def calculate_values(systems):
        names = []
        colours = []
        values = []

        for system in sorted(systems):
            system_cost = 0.0

            for component in system.get_components():
                # use of tablecost instead of unitcost not to include the cost
                # of parts twice in the system cost
                system_cost += component.tablecost * component.quantity

            names.append(system.name)
            colours.append((system.colour[0] / 255.0, system.colour[1] / 255.0, system.colour[2] / 255.0))
            values.append(system_cost)

        return names, colours, values

    figure(1, figsize=(10, 7), facecolor='w')
    axes([0.1, 0.1, 0.6, 0.8])

    names, colours, values = calculate_values(systems)
    labels = ['%.2f$' % value for value in values]

    patches, _texts, _autotexts = \
        pie(values, labels=labels, colors=colours, autopct='%1.1f%%', shadow=True)

    figlegend(patches, names, 'center right')

    path = os.path.join(basepath, "cost_summary.pdf")
    savefig(path)

