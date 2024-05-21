.. MatFeaLib documentation master file, created by
   sphinx-quickstart on Mon Mar 18 21:25:58 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. Welcome to MatFeaLib's documentation!
.. =====================================



.. image:: ./_static/MatFeaLib.png
   :width: 450 px
   :alt: MatFeaLib
   :align: center

|

MatFeaLib
============

**MatFeaLib** (**Mat**\erials **Fea**\ture **Lib**\rary) is a Python library for generating elemental features from materials composition. These representations are often called “descriptors” and can be used in machine learning and data analysis in Materials Science. To get started you can check the :ref:`basic usage </notebooks/usage.ipynb>`.


.. note::

   This project is under active development.


It has the following capabilities:

- Generation of primary atomic features of any given compound, a given list of materials, and  a given pandas dataframe
- Generation of atomic features in statistical form 

It can also be used by any user-specified atomic feature collection. 


+-------------------------------+------------------------------------------------------------------------------------------------------------+
| Feature Collection            | Description                                                                                                |
+===============================+============================================================================================================+
| dft_pbe (dft_pbe_spins)       | The DFT calculated atomic properties by using the PBE approximation,                                       |
|                               |                                                                                                            |
|                               | accessible from FHI as the source                                                                          |
|                               | (`source <https://gitlab.mpcdf.mpg.de/nomad-lab/atomic_features_fhi_aims_really_tight/-/tree/master/csv>`_)|
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| dft_hse06 (dft_hse06_spins)   | The DFT calculated atomic properties by using the HSE06 hybrid                                             |
|                               |                                                                                                            |
|                               | functional, accessible from FHI as the source                                                              |
|                               | (`source <https://gitlab.mpcdf.mpg.de/nomad-lab/atomic_features_fhi_aims_really_tight/-/tree/master/csv>`_)|
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| dft_pbe0 (dft_pbe0_spins)     | The DFT calculated atomic properties by using the PBE0 hybrid                                              |
|                               |                                                                                                            |
|                               | functional, accessible from FHI as the source                                                              |
|                               | (`source <https://gitlab.mpcdf.mpg.de/nomad-lab/atomic_features_fhi_aims_really_tight/-/tree/master/csv>`_)|
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| dft_pbesol (dft_pbesol_spins) | The DFT calculated atomic properties by using the PBEsol                                                   |
|                               |                                                                                                            |
|                               | approximation, accessible from FHI as the source                                                           |
|                               | (`source <https://gitlab.mpcdf.mpg.de/nomad-lab/atomic_features_fhi_aims_really_tight/-/tree/master/csv>`_)|
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| dft_pwlda (dft_pwlda_spins)   | The DFT calculated atomic properties by using the Local-density                                            |
|                               |                                                                                                            |
|                               | approximation (LDA) parameterized by Perdew and Wang (PW),                                                 |
|                               |                                                                                                            |
|                               | accessible from FHI as the source                                                                          |
|                               | (`source <https://gitlab.mpcdf.mpg.de/nomad-lab/atomic_features_fhi_aims_really_tight/-/tree/master/csv>`_)|
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| dft_revpbe (dft_revpbe_spins) | The DFT calculated atomic properties by using the revPBE                                                   |
|                               |                                                                                                            |
|                               | approximation, accessible from FHI as the source                                                           |
|                               | (`source <https://gitlab.mpcdf.mpg.de/nomad-lab/atomic_features_fhi_aims_really_tight/-/tree/master/csv>`_)|
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| lda2015                       | The DFT calculated atomic properties by using the Local-density                                            |
|                               |                                                                                                            |
|                               | approximation, accessible from the PRL paper as the source                                                 |
|                               |                                                                                                            |
|                               | (`source <https://doi.org/10.1103/PhysRevLett.114.105503>`_)                                               |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| Mendeleev                     | The atomic properties from the mendeleev package                                                           |
|                               | (`source <https://mendeleev.readthedocs.io/en/stable/>`_)                                                  |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| Matminer                      | The atomic properties from the matminer package                                                            |
|                               | (`source <https://hackingmaterials.lbl.gov/matminer/>`_)                                                   |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| Pymatgen                      | The atomic properties from the pymatgen package                                                            |
|                               | (`source <https://pymatgen.org>`_)                                                                         |
+-------------------------------+------------------------------------------------------------------------------------------------------------+

Get started
-----------
- :doc:`Installation and Setup </installation>`
- :doc:`Tutorial </tutorial>`
- :doc:`Usage </notebooks/usage>`

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Getting started

   installation
   tutorial
   notebooks/usage

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`





