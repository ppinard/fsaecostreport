#!/usr/bin/env python
"""
================================================================================
:mod:`build` -- Distribution builder
================================================================================

.. module:: build
   :synopsis: Distribution builder

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import zipfile
import shutil

# Third party modules.
from pkg_resources import to_filename

# Local modules.
from setuputilities.builder import SetupBuild, BaseBuild, DocBuild, TestBuild
from setuputilities.builder.py2exe import Py2exeBuild
from setuputilities.util import find_package_path, find_packages, find_package_data

# Globals and constants variables.

class Build(BaseBuild, SetupBuild, DocBuild, TestBuild, Py2exeBuild):
    PROJECT_DIR = find_package_path('fsaecostreport')

    def __init__(self):
        BaseBuild.__init__(self)
        SetupBuild.__init__(self)
        DocBuild.__init__(self)
        TestBuild.__init__(self)
        Py2exeBuild.__init__(self)

        # Base Build
        self.metadata.name = "fsaecostreport"
        self.metadata.version = "0.1"
        self.metadata.author = "Philippe T. Pinard"
        self.metadata.author_email = "philippe.pinard@gmail.com"
        self.metadata.description = "Generator of the FSAE Cost Report"
        self.metadata.license = "GPL v3"
        self.metadata.classifiers = [
                "Development Status :: 4 - Beta",
                "License :: OSI Approved :: GNU General Public License (GPL)",
                "Natural Language :: English",
                "Operating System :: OS Independent",
                "Programming Language :: Python",
                "Topic :: Software Development"]
        self.metadata.platforms = "Windows OS"

        # Setup Build
        self.packages = find_packages("fsaecostreport",
                                      where=self.PROJECT_DIR)
        self.package_data = find_package_data(package='fsaecostreport',
                                              where=self.PROJECT_DIR)

        # Doc Build
        self.doc_dir = os.path.join(self.PROJECT_DIR, 'doc')

        # py2exe
        self.console_scripts = [os.path.join(self.PROJECT_DIR, 'app.py')]

    def bdist_exe(self):
        Py2exeBuild.bdist_exe(self)

        # rename app.exe to costreport-app.exe
        old = os.path.join(self.dest_dir, 'app.exe')
        new = os.path.join(self.dest_dir, 'costreport-app.exe')
        os.rename(old, new)

        # zip the dest
        filename = '%s-%s.zip' % (to_filename(self.metadata.name),
                                  to_filename(self.metadata.version))
        zip = zipfile.ZipFile(os.path.join(self.dest_dir, filename), mode='w')

        # walk through the file and folders in dest
        for root, _dirs, files in os.walk(self.dest_dir):
            for fn in files:
                if fn == filename:
                    continue

                abspath = os.path.join(root, fn)
                relpath = abspath[len(self.dest_dir) + len(os.sep):]
                relpath = os.path.join('bin', relpath)
                zip.write(abspath, relpath)

        zip.close()

        # clean up
        for name in os.listdir(self.dest_dir):
            path = os.path.join(self.dest_dir, name)

            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path) and name != filename:
                os.remove(path)

if __name__ == '__main__':
    build = Build()
    build.run()
