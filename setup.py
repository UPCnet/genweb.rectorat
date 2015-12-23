# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.5.3.dev0'

README = open("README.rst").read()
HISTORY = open(os.path.join("docs", "HISTORY.rst")).read()

setup(name='genweb.rectorat',
      version=version,
      description="Bases de dades documentals migrada de Lotus Notes",
      long_description=README + "\n" + HISTORY,
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='Bases de dades documentals',
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://github.com/UPCnet/genweb.rectorat',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['genweb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'five.grok',
          'plone.app.dexterity [grok]',
          'plone.formwidget.multifile',
          'collective.dexteritytextindexer',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
