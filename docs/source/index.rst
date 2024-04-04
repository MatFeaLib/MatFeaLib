.. MatFeaLib documentation master file, created by
   sphinx-quickstart on Mon Mar 18 21:25:58 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. Welcome to MatFeaLib's documentation!
.. =====================================



.. image:: ./_static/MatFeaLib-logo-04.png
   :width: 903 px
   :alt: MatFeaLib
   :align: center

|

MatFeaLib
============

**MatFeaLib** (**Mat**\erials **Fea**\ture **Lib**\rary) is a Python library for generating elemental features from materials composition. These representations are often called “descriptors” and can be used in machine learning and data analysis in Materials Science. To get started you can check the basic tutorial.


.. note::

   This project is under active development.


It has the following capabilities:

- Generation of primary atomic features of any given compound, a given list of materials, and  a given pandas dataframe
- Generation of atomic features in statistical form 


MatFeaLib currently includes the following atomic feature collections:

.. list-table::
   :widths: 80 10
   :header-rows: 1

   * - Feature Collection
     - Features
   * - Mendeleev
     - ✓
   * - Matminer
     - ✓
   * - Pymatgen
     - ✓

It can also be used by any user-specified atomic feature collection. 

Get started
-----------
- :doc:`Installation and Setup </installation>`
- :doc:`Tutorial </usage>`

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Getting started

   installation
   usage


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`





