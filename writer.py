#!/usr/bin/env python
"""
================================================================================
:mod:`writer` -- LaTeX writer of the cost report
================================================================================

.. module:: writer
   :synopsis: LaTeX writer of the cost report

.. inheritance-diagram:: fsaecostreport.writer

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import operator
import posixpath
import os.path

# Third party modules.

# Local modules.
from misctools.format import humanjoin

from fsaecostreport.latex import create_tabular, escape as e
from fsaecostreport.component import Part, Assembly

# Globals and constants variables.
from constants import DRAWINGS_DIR, PICTURES_DIR, LOGO_FILE
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
    def write(self, basepath, systems, metadata):
        filename = 'costreport%i.tex' % metadata.year
        lines = self._write(systems, metadata)

        with open(os.path.join(basepath, filename), 'w') as out:
            for line in lines:
                out.write(line + "\n")
        out.close()

    def _write(self, systems, metadata):
        lines = []

        lines += self.write_header(metadata.year)
        lines += ['']

        lines += [r'\begin{document}']
        lines += ['']

        lines += self.write_fancy_header(metadata.year, metadata.team_name)
        lines += ['']
        lines += self.write_renewcommand()
        lines += ['']
        lines += self.write_colors(systems)
        lines += ['']

        # content
        lines += self.write_frontmatter(systems, metadata.introduction)
        lines += ['']

        lines += self.write_systems(systems)
        lines += ['']

        lines += self.write_backmatter()
        lines += ['']

        lines += [r'\end{document}']

        return lines

    def write_header(self, year):
        lines = []

        lines += [r'\documentclass[letterpaper,landscape]{report}']

        lines += [r'\usepackage[top=3cm, bottom=3cm, right=1cm, left=1cm]{geometry}']
        lines += [r'\usepackage{graphicx}']
        lines += [r'\usepackage{multirow}']
        lines += [r'\usepackage{url}']
        lines += [r'\usepackage{amsmath}']
        lines += [r'\usepackage{longtable}']
        lines += [r'\usepackage{titlesec}']
        lines += [r'\usepackage{array}']
        lines += [r'\usepackage{colortbl}']
        lines += [r'\usepackage{multicol}']
        lines += [r'\usepackage{setspace}']
        lines += [r'\usepackage[final]{pdfpages}']
        lines += [r'\usepackage[english]{babel}']
        lines += [r'\usepackage[latin1]{inputenc}']
        lines += [r'\usepackage{fancyhdr}']
        lines += [r'\usepackage[pdftitle={Cost Report %i}, ' % year,
                  r'pdfsubject={Formula SAE Competition Michigan}, ',
                  r'pdfauthor={McGill Racing Team}, ',
                  r'colorlinks=true, ',
                  r'linkcolor=blue, ',
                  r'pdfborder = 0 0 0, ',
                  r'pdfhighlight = /I, ',
                  r'pdfpagelabels]{hyperref}']

        return lines

    def write_fancy_header(self, year, team_name):
        lines = []

        lines += [r'\pagestyle{fancy}']
        lines += [r'\fancyhf{}']
        lines += [r'\lhead{\includegraphics[height=0.25cm]{%s} %s -- %i Cost Report}' % (LOGO_FILE, team_name, year)]
        lines += [r'\lfoot{\small\nouppercase{\leftmark}}']
        lines += [r'\rfoot{\thepage}']
        lines += [r'\fancypagestyle{plain}{']
        lines += [r'\fancyhf{}']
        lines += [r'\lhead{\includegraphics[height=0.25cm]{%s} %s -- %i Cost Report}' % (LOGO_FILE, team_name, year)]
        lines += [r'\lfoot{\small\nouppercase{\leftmark}}']
        lines += [r'\rfoot{\thepage}}']

        return lines

    def write_renewcommand(self):
        lines = []

        lines += [r'\renewcommand{\chaptername}{\sffamily System}']
        lines += [r'\renewcommand{\thechapter}{\Alph{chapter}}']
        lines += [r'\titleformat*{\section}{\Large\sffamily\raggedright}']
        lines += [r'\renewcommand{\chaptermark}[1]{\markboth{\chaptername\ \thechapter:\ #1}{}}']
        lines += [r'\titlespacing{\subsubsection}{0pt}{*1}{*-1}']

        return lines

    def write_colors(self, systems):
        lines = []

        for system in sorted(systems):
            r = system.colour[0] / 255.0
            g = system.colour[1] / 255.0
            b = system.colour[2] / 255.0
            lines += [r'\definecolor{color%s}{rgb}{%f,%f,%f}' % \
                        (system.letter, r, g, b)]

        return lines

    def write_frontmatter(self, systems, introduction):
        lines = []

        lines += [r'\pagenumbering{roman}']
        lines += ['']

        lines += self.write_introduction(introduction)
        lines += [r'\newpage', '']

        lines += self.write_cost_summary(systems)
        lines += [r'\newpage', '']

        lines += self.write_standard_partnumbering()
        lines += [r'\newpage', '']

        lines += self.write_toc()
        lines += [r'\newpage', '']

        lines += [r'\pagenumbering{arabic}']

        return lines

    def write_introduction(self, introduction):
        lines = []

        lines += [r'\section{Introduction}']
        lines += [r'\begin{multicols}{2}]']

        lines += introduction

        lines += [r'\end{multicols}']

        return lines

    def write_cost_summary(self, systems):
        lines = []

        lines += [r'\section{Cost Summary}']
        lines += [r'\renewcommand{\arraystretch}{1.5}']

        data = self._create_cost_summary_lines(systems)
        lines += \
            create_tabular(data, environment='longtable',
                               tableparameters='l',
                               tablespec=r'p{20em} | p{8em} | p{8em} | p{8em} | p{8em} | p{12em}',
                               format_before_tabular=r'\rowcolor[gray]{0}',
                               format_after_header=r'\hline\endhead',
                               format_between_rows=r'\hline', header_endrow=1)
        lines += [r'\renewcommand{\arraystretch}{1}']

        return lines

    def _create_cost_summary_lines(self, systems):
        rows = []

        header = [r'\color{white} System',
                  r'\color{white}\centering Materials',
                  r'\color{white}\centering Processes',
                  r'\color{white}\centering Fasteners',
                  r'\color{white}\centering Tooling',
                  r'\color{white}\centering Total']
        rows.append(header)

        materials_totalcost = 0.0
        processes_totalcost = 0.0
        fasteners_totalcost = 0.0
        toolings_totalcost = 0.0
        systems_totalcost = 0.0

        for system in sorted(systems):
            materials_cost = 0.0
            processes_cost = 0.0
            fasteners_cost = 0.0
            toolings_cost = 0.0
            system_cost = 0.0

            for component in system.get_components():
                qty = component.quantity
                materials_cost += sum(map(SUBTOTAL, component.materials)) * qty
                processes_cost += sum(map(SUBTOTAL, component.processes)) * qty
                fasteners_cost += sum(map(SUBTOTAL, component.fasteners)) * qty
                toolings_cost += sum(map(SUBTOTAL, component.toolings)) * qty
                system_cost += component.unitcost * qty


            row = [r'\rowcolor{color%s}\raggedright %s' % (system.letter, system.name),
                   r'\centering\$ %4.2f' % materials_cost,
                   r'\centering\$ %4.2f' % processes_cost,
                   r'\centering\$ %4.2f' % fasteners_cost,
                   r'\centering\$ %4.2f' % toolings_cost,
                   r'\centering\$ %4.2f' % system_cost]
            rows.append(row)

            materials_totalcost += materials_cost
            processes_totalcost += processes_cost
            fasteners_totalcost += fasteners_cost
            toolings_totalcost += toolings_cost
            systems_totalcost += system_cost


        row = [r'\hline\raggedright\textbf{ % s}' % 'Total Vehicle',
               r'\centering\textbf{\$ %4.2f}' % materials_totalcost,
               r'\centering\textbf{\$ %4.2f}' % processes_totalcost,
               r'\centering\textbf{\$ %4.2f}' % fasteners_totalcost,
               r'\centering\textbf{\$ %4.2f}' % toolings_totalcost,
               r'\centering\textbf{\$ %4.2f}' % toolings_totalcost]
        rows.append(row)

        return rows

    def write_standard_partnumbering(self):
        #TODO: Standard part numbering
        return []

    def write_toc(self):
        lines = []

        lines += [r'\setcounter{tocdepth}{1}']
        lines += [r'\tableofcontents']
        lines += [r'\pdfbookmark[0]{Contents}{contents}']
        lines += [r'\newpage']
        lines += [r'\setcounter{tocdepth}{4}']
        lines += ['']

        return lines

    def write_systems(self, systems):
        lines = []

        for system in sorted(systems):
            lines += SystemLaTeXWriter().write(system)
            lines += ['']

        return lines

    def write_backmatter(self):
        lines = []

        lines += [r'\renewcommand{\listfigurename}{List of Drawings}']
        lines += [r'\listoffigures']
        lines += [r'\pdfbookmark[0]{List of Drawings}{listofdd}']

        return lines


class SystemLaTeXWriter(object):
    def write(self, system):
        hierarchy = system.get_hierarchy()

        lines = []

        lines += [r'\chapter{%s}' % system.name]
        lines += [r'\newpage', '']

        # BOM
        lines += self.write_bom(system, hierarchy)
        lines += [r'\newpage', '']

        # cost tables
        lines += self.write_costtables(system, hierarchy)
        lines += [r'\newpage', '']

        # drawings
        lines += self.write_drawings(system, hierarchy)
        lines += [r'\newpage', '']

        # pictures
        lines += self.write_pictures(system, hierarchy)
        lines += [r'\newpage', '']

        return lines

    def write_bom(self, system, hierarchy):
        lines = []

        lines += [r'\section{BOM}']
        lines += [r'\renewcommand{\arraystretch}{1.1}']

        data = self._create_bom_lines(system, hierarchy)
        lines += \
            create_tabular(data, environment='longtable',
                               tableparameters='l',
                               tablespec=r'p{10em} | p{3em} | p{2em} | p{7em} | p{13em} | p{2em} | p{4.5em} | p{4.5em} | p{5em} | p{5em} | p{5em}',
                               format_before_tabular=r'\rowcolor[gray]{0}',
                               format_after_header=r'\hline\endhead',
                               format_between_rows=r'\hline', header_endrow=1)

        lines += [r'\renewcommand{\arraystretch}{1}']

        return lines

    def _create_bom_lines(self, system, hierarchy):
        rows = []

        header = [r'\color{white} Component',
                  r'\color{white}\centering Asm / Prt \#',
                  r'\color{white}\centering Rev.',
                  r'\color{white}\centering Assembly',
                  r'\color{white} Description',
                  r'\color{white}\centering Qty',
                  r'\color{white}\centering Unit\\ Cost',
                  r'\color{white}\centering Cost',
                  r'\color{white}\centering Cost\\ Table',
                  r'\color{white}\centering Drawing(s)',
                  r'\color{white}\centering Photo(s)']
        rows.append(header)


        for component in hierarchy:
            if len(component.drawings) == 1:
                drawings = r'\pageref{dwg:%s-0}' % component.pn
            elif len(component.drawings) > 1:
                drawings = r'\pageref{dwg:%s-0}--\pageref{dwg:%s-%i}' % \
                        (component.pn, component.pn, len(component.drawings) - 1)
            else:
                drawings = ''

            if len(component.pictures) == 1:
                pictures = r'\pageref{img:%s-0}' % component.pn
            elif len(component.pictures) > 1:
                pictures = r'\pageref{img:%s-0}--\pageref{img:%s-%i}' % \
                        (component.pn, component.pn, len(component.pictures) - 1)
            else:
                pictures = ''

            unitcost = component.unitcost
            quantity = component.quantity
            totalcost = unitcost * quantity

            names = [e(capitalize(parent.name)) for parent in component.parents]
            assembly = humanjoin(names, andchr=r'\&')

            if isinstance(component, Assembly):
                row = [r'\hline\emph{%s}' % e(capitalize(component.name))]
            elif isinstance(component, Part):
                row = [r'%s' % e(capitalize(component.name))]

            row += [r'\centering %s' % component.pn_base,
                    r'\centering %s' % component.revision,
                    r'\centering %s' % assembly,
                    r'\raggedright %s' % e(capitalize(component.details)),
                    r'\centering %i' % quantity,
                    r'\raggedleft\$ %4.2f' % unitcost,
                    r'\raggedleft\$ %4.2f' % totalcost,
                    r'\centering\pageref{ct:%s}' % component.pn,
                    r'\centering%s' % drawings,
                    r'\centering%s' % pictures]
            rows.append(row)

        return rows

    def write_costtables(self, system, hierarchy):
        lines = []

        lines += [r'\section{Cost Tables}']

        for component in hierarchy:
            if isinstance(component, Assembly):
                lines += AssemblyLaTeXWriter().write_costtables(component)
            elif isinstance(component, Part):
                lines += PartLaTeXWriter().write_costtables(component)

        return lines

    def write_drawings(self, system, hierarchy):
        lines = []

        lines += [r'\section{Technical Drawings}']
        lines += ['The technical drawings are in the following pages.']

        for component in hierarchy:
            name = component.name.replace(',', '')
            pn = component.pn

            for index, drawing in enumerate(component.drawings):
                path = posixpath.join(system.label, DRAWINGS_DIR, os.path.basename(drawing))
                lines += [r'\includepdf[pages={1}, addtolist={1,figure,%s (%s),dwg:%s-%i}]{%s}' % \
                          (name, pn, pn, index, path)]
                lines += [r'\addcontentsline{toc}{subsection}{%s (%s)}' % \
                          (name, pn)]

        return lines

    def write_pictures(self, system, hierarchy):
        lines = []

        lines += [r'\section{Pictures}']

        for component in hierarchy:
            name = component.name
            pn = component.pn

            for index, picture in enumerate(component.pictures):
                path = posixpath.join(system.label, PICTURES_DIR, os.path.basename(picture))
                lines += [r'\subsection{%s (%s)}' % (name, pn)]
                lines += [r'\label{img:%s-%i}' % (pn, index)]
                lines += [r'\begin{center}']
                lines += [r'\includegraphics[height=0.8\textheight]{%s}' % path]
                lines += [r'\end{center}']
                lines += [r'\newpage']

        return lines

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

# TODO: eBOM writer
class eBOMWriter(object):
    def write(self, basepath, systems, metadata):
        pass
