#!/usr/bin/env python
"""
================================================================================
:mod:`writer` -- 
================================================================================

.. module:: writer
   :synopsis: 

.. inheritance-diagram:: writer

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import operator

# Third party modules.

# Local modules.
from latex import create_tabular, escape as e

# Globals and constants variables.
SUBTOTAL = operator.attrgetter('subtotal')

def decimal(number):
    if number < 0.01:
        return '%.2e' % number
    else:
        return '%4.2f' % number

def capitalize(value):
    if value:
        return value[0].upper() + value[1:]
    else:
        return value

class CostReportLaTeXWriter(object):
    def write(self, config):
        pass

    def write_frontmatter(self):
        return []

    def _create_toc_lines(self):
        lines = []

        lines += [r'\setcounter{tocdepth}{1}']
        lines += [r'\tableofcontents']
        lines += [r'\pdfbookmark[0]{Contents}{contents}']
        lines += [r'\newpage', '']
        lines += [r'\setcounter{tocdepth}{4}']
        lines += [r'\pagenumbering{arabic}']
        lines += ['']

        return lines

    def write_systems(self, systems):
        lines = []
        writer = SystemLaTeXWriter()

        for system in sorted(systems):
            lines += writer.write(system)
            lines += ['']

        return lines

    def write_backmatter(self):
        lines = []

        lines += [r'\renewcommand{\listfigurename}{List of Drawings}']
        lines += [r'\listoffigures']
        lines += [r'\pdfbookmark[0]{List of Drawings}{listofdd}']
        lines += [r'\newpage', '']

        return lines


class SystemLaTeXWriter(object):
    def write(self, system):
        lines = []

        lines += [r'\chapter{%s}' % system.name]
        lines += [r'\newpage', '']

        # BOM
        lines += [r'\section{BOM}']
        lines += self.write_bom(system)
        lines += [r'\newpage', '']

        # cost tables
        lines += [r'\section{Cost Tables}']
        lines += self.write_costtables(system)
        lines += [r'\newpage', '']

        # drawings
        lines += [r'\section{Technical Drawings}']
        lines += ['The technical drawings are in the following pages.']
        lines += self.write_drawings(system)
        lines += [r'\newpage', '']

        # pictures
        lines += [r'\section{Pictures}']
        lines += self.write_pictures(system)
        lines += [r'\newpage', '']

        return lines

    def write_bom(self, system):
        return []

    def write_costtables(self, system):
        return []

    def write_drawings(self, system):
        return []

    def write_pictures(self, system):
        return []

class _ComponentLaTeXWriter(object):
    def write_costtables(self, component):
        lines = []

        lines += self._create_header_lines(component)

        lines += self.write_materials(component.materials)
        lines += self.write_processes(component.processes)
        lines += self.write_fasteners(component.fasteners)
        lines += self.write_toolings(component.toolings)

        return lines

    def _create_header_lines(self, component):
        lines = []

        lines += [r'\subsection{%s (%s)}' % (component.name, component.pn)]
        lines += [r'\label{ct:%s}' % component.pn]

        return lines

    def write_materials(self, materials):
        lines = []

        if materials:
            lines += [r'\subsubsection*{Materials}']
            lines += [r'\renewcommand{\arraystretch}{1.25}']

            data = self._create_materials_rows(materials)
            lines += \
                create_tabular(data, environment='longtable',
                               tableparameters='l',
                               tablespec=r'm{14em}|m{12em}|m{6em}|m{6em}|m{4.5em}|m{4.5em}|m{4.5em}',
                               format_before_tabular=r'\rowcolor[gray]{0}',
                               format_after_header=r'\hline\endhead',
                               format_between_rows=r'\hline', header_endrow=1)

            lines += [r'\renewcommand{\arraystretch}{1}']

        lines += ['']

        return lines

    def _create_materials_rows(self, materials):
        rows = []

        # header
        header = [r'\color{white} Material',
                  r'\color{white} Use',
                  r'\color{white}\centering Size 1',
                  r'\color{white}\centering Size 2',
                  r'\color{white}\centering Unit Cost',
                  r'\color{white}\centering Qty',
                  r'\color{white}\centering Sub Total']
        rows.append(header)

        # rows
        for material in materials:
            if material.size1:
                size1 = '%s $%s$' % (decimal(material.size1), e(material.unit1))
            else:
                size1 = r'\ '

            if material.size2:
                size2 = '%s $%s$' % (decimal(material.size2), e(material.unit2))
            else:
                size2 = r'\ '

            row = [r'\raggedright %s' % e(capitalize(material.name)),
                   r'\raggedright %s' % e(capitalize(material.use)),
                   r'\centering %s' % size1,
                   r'\centering %s' % size2,
                   r'\raggedleft\$ %4.2f' % material.unitcost,
                   r'\centering %s' % material.quantity,
                   r'\raggedleft\$ %4.2f' % material.subtotal]
            rows.append(row)

        # total
        totalcost = sum(map(SUBTOTAL, materials))
        row = [r'\multicolumn{6}{r}{\textbf{Total}}',
               r'\raggedleft\textbf{\$ %4.2f}' % totalcost]
        rows.append(row)

        return rows

    def write_processes(self, processes):
        lines = []

        if processes:
            lines += [r'\subsubsection*{Processes}']
            lines += [r'\renewcommand{\arraystretch}{1.25}']

            data = self._create_processes_rows(processes)
            lines += \
                create_tabular(data, environment='longtable',
                               tableparameters='l',
                               tablespec=r'm{14em}|m{12em}|m{6em}|m{6em}|m{4.5em}|m{4.5em}',
                               format_before_tabular=r'\rowcolor[gray]{0}',
                               format_after_header=r'\hline\endhead',
                               format_between_rows=r'\hline', header_endrow=1)

            lines += [r'\renewcommand{\arraystretch}{1}']

        lines += ['']

        return lines

    def _create_processes_rows(self, processes):
        rows = []

        # header
        header = [r'\color{white} Process',
                  r'\color{white} Use',
                  r'\color{white}\centering Cost',
                  r'\color{white}\centering Qty',
                  r'\color{white}\centering Multiplier',
                  r'\color{white}\centering Sub Total']
        rows.append(header)

        # rows
        for process in processes:
            unitcost = r'\$ %4.2f / $%s$' % (process.unitcost, e(process.unit))

            if process.multiplier is None:
                multiplier = 1.0
            else:
                multiplier = '%4.2f' % process.multiplier


            row = [r'\raggedright %s' % e(capitalize(process.name)),
                   r'\raggedright %s' % e(capitalize(process.use)),
                   r'\raggedleft %s' % unitcost,
                   r'\centering %4.2f' % process.quantity,
                   r'\centering %s' % multiplier,
                   r'\raggedleft\$ %4.2f' % process.subtotal]
            rows.append(row)

        # total
        totalcost = sum(map(SUBTOTAL, processes))
        row = [r'\multicolumn{5}{r}{\textbf{Total}}',
               r'\raggedleft\textbf{\$ %4.2f}' % totalcost]
        rows.append(row)

        return rows

    def write_fasteners(self, fasteners):
        lines = []

        if fasteners:
            lines += [r'\subsubsection*{Fasteners}']
            lines += [r'\renewcommand{\arraystretch}{1.25}']

            data = self._create_fasteners_rows(fasteners)
            lines += \
                create_tabular(data, environment='longtable',
                               tableparameters='l',
                               tablespec=r'm{14em}|m{12em}|m{6em}|m{6em}|m{4.5em}|m{4.5em}|m{4.5em}',
                               format_before_tabular=r'\rowcolor[gray]{0}',
                               format_after_header=r'\hline\endhead',
                               format_between_rows=r'\hline', header_endrow=1)

            lines += [r'\renewcommand{\arraystretch}{1}']

        lines += ['']

        return lines

    def _create_fasteners_rows(self, fasteners):
        rows = []

        # header
        header = [r'\color{white} Fastener',
                  r'\color{white} Use',
                  r'\color{white}\centering Size 1',
                  r'\color{white}\centering Size 2',
                  r'\color{white}\centering Cost',
                  r'\color{white}\centering Qty',
                  r'\color{white}\centering Sub Total']
        rows.append(header)

        # rows
        for fastener in fasteners:
            if fastener.size1 is not None:
                size1 = '%4.2f $%s$' % (fastener.size1, e(fastener.unit1))
            else:
                size1 = r'\ '
            if fastener.size2 is not None:
                size2 = '%4.2f $%s$' % (fastener.size2, e(fastener.unit2))
            else:
                size2 = r'\ '

            row = [r'\raggedright %s' % e(capitalize(fastener.name)),
                   r'\raggedright %s' % e(capitalize(fastener.use)),
                   r'\centering %s' % size1,
                   r'\centering %s' % size2,
                   r'\raggedleft\$ %4.2f' % fastener.unitcost,
                   r'\centering %s' % fastener.quantity,
                   r'\raggedleft\$ %4.2f' % fastener.subtotal]
            rows.append(row)

        # total
        totalcost = sum(map(SUBTOTAL, fasteners))
        row = [r'\multicolumn{6}{r}{\textbf{Total}}',
               r'\raggedleft\textbf{\$ %4.2f}' % totalcost]
        rows.append(row)

        return rows

    def write_toolings(self, toolings):
        lines = []

        if toolings:
            lines += [r'\subsubsection*{Tooling}']
            lines += [r'\renewcommand{\arraystretch}{1.25}']

            data = self._create_toolings_rows(toolings)
            lines += \
                create_tabular(data, environment='longtable',
                               tableparameters='l',
                               tablespec=r'm{14em}|m{12em}|m{8em}|m{6em}|m{6em}|m{4.5em}',
                               format_before_tabular=r'\rowcolor[gray]{0}',
                               format_after_header=r'\hline\endhead',
                               format_between_rows=r'\hline', header_endrow=1)

            lines += [r'\renewcommand{\arraystretch}{1}']

        lines += ['']

        return lines

    def _create_toolings_rows(self, toolings):
        rows = []

        # header
        header = [r'\color{white} Tooling',
                  r'\color{white} Use',
                  r'\color{white}\centering Unit Cost',
                  r'\color{white}\centering Qty',
                  r'\color{white}\centering PVF',
                  r'\color{white}\centering Sub Total']
        rows.append(header)

        # rows
        for tooling in toolings:
            unitcost = r'\$ %4.2f / $%s$' % (tooling.unitcost, e(tooling.unit))


            row = [r'\raggedright %s' % e(capitalize(tooling.name)),
                   r'\raggedright %s' % e(capitalize(tooling.use)),
                   r'\raggedleft %s' % unitcost,
                   r'\centering %s' % tooling.quantity,
                   r'\centering %s' % tooling.pvf,
                   r'\raggedleft\$ %4.2f' % tooling.subtotal]
            rows.append(row)

        # total
        totalcost = sum(map(SUBTOTAL, toolings))
        row = [r'\multicolumn{5}{r}{\textbf{Total}}',
               r'\raggedleft\textbf{\$ %4.2f}' % totalcost]
        rows.append(row)

        return rows

    def write_drawings(self):
        pass

    def write_pictures(self):
        pass

class AssemblyLaTeXWriter(_ComponentLaTeXWriter):
    def write_costtables(self, component):
        lines = []

        lines += self._create_header_lines(component)

        lines += self.write_parts(component.components)
        lines += self.write_materials(component.materials)
        lines += self.write_processes(component.processes)
        lines += self.write_fasteners(component.fasteners)
        lines += self.write_toolings(component.toolings)

        return lines

    def write_parts(self, parts):
        lines = []

        if parts:
            lines += [r'\subsubsection*{Parts}']
            lines += [r'\renewcommand{\arraystretch}{1.25}']

            data = self._create_parts_rows(parts)
            lines += \
                create_tabular(data, environment='longtable',
                               tableparameters='l',
                               tablespec=r'm{14em}|m{8em}|m{6em}|m{4.5em}|m{4.5em}',
                               format_before_tabular=r'\rowcolor[gray]{0}',
                               format_after_header=r'\hline\endhead',
                               format_between_rows=r'\hline', header_endrow=1)

            lines += [r'\renewcommand{\arraystretch}{1}']

        lines += ['']

        return lines

    def _create_parts_rows(self, parts):
        rows = []

        # header
        header = [r'\color{white} Part',
                  r'\color{white}\centering Part Number',
                  r'\color{white}\centering Part Cost',
                  r'\color{white}\centering Qty',
                  r'\color{white}\centering Sub Total']
        rows.append(header)

        # rows
        totalcost = 0.0

        for part, quantity in parts.iteritems():
            subtotal = part.unitcost * quantity

            row = [r'\raggedright %s' % e(capitalize(part.name)),
                   r'\centering %s' % part.pn,
                   r'\raggedleft\$ %4.2f' % part.unitcost,
                   r'\centering %s' % quantity,
                   r'\raggedleft\$ %4.2f' % subtotal]
            rows.append(row)

            totalcost += subtotal

        # total
        row = [r'\multicolumn{4}{r}{\textbf{Total}}',
               r'\raggedleft\textbf{\$ %4.2f}' % totalcost]
        rows.append(row)

        return rows

class PartLaTeXWriter(_ComponentLaTeXWriter):
    pass
