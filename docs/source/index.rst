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

**MatFeaLib** (**Mat**\erials **Fea**\tures **Lib**\rary) is a Python library for generating elemental features from materials composition. These representations are often called “descriptors” and can be used in machine learning and data analysis in Materials Science. To get started you can check the :ref:`basic usage </notebooks/usage.ipynb>`.


.. note::

   This project is under active development.


It has the following capabilities:

- Generation of primary atomic features of any given compound, a given list of materials, and  a given pandas dataframe
- Generation of atomic features in statistical form 
- Visualizing the periodic table of elements

MatFeaLib currently includes the following atomic feature collections:

+-------------------------------+------------------------------------------------------------------------------------------------------------+
| Feature Collection            | Description                                                                                                |
+===============================+============================================================================================================+
| dft_pbe (dft_pbe_spins)       | The DFT calculated atomic properties by using the PBE                                                      |
|                               |                                                                                                            |
|                               | approximation, accessible from FHI as the source                                                           |
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

It can also be used by any user-specified atomic feature collection. 

The statistical measures of atomic features are useful for multi-stoichiometric material data. The MatFeaLib support the following statistics:

+-------------------------------+------------------------------------------------------------------------------------------------------------+
| Feature Collection            | Description                                                                                                |
+===============================+============================================================================================================+
| min                           | The maximum value                                                                                          |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| max                           | The minimum value                                                                                          |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| sum                           | The summation of values                                                                                    |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| mean                          | The arithmetic mean                                                                                        |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| std                           | The standard deviation                                                                                     |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| var                           | The unbiased variance                                                                                      |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| median                        | The middle value                                                                                           |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| diff                          | The difference between maximum and minimum values                                                          |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| gmean                         | The geometric mean                                                                                         |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| hmean                         | The harmonic mean                                                                                          |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| pmean                         | The power mean                                                                                             |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| Kurtosis                      | The fourth central moment divided by the square of the variance                                            |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| moment                        | It is a specific quantitative measure of the shape of a set of points.                                     |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| expectile                     | The Expectiles; They are a generalization of the expectation, in the same way as                           |
|                               |                                                                                                            |
|                               | quantiles are a generalization of the median.                                                              |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| skew                          | For normally distributed data, the skewness should be about zero. For unimodal                             |
|                               |                                                                                                            |
|                               | continuous distributions, a skewness value greater than zero means that there                              |
|                               |                                                                                                            |
|                               | is more weight in the distribution's right tail.                                                           |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| gstd                          | The geometric standard deviation; It describes the spread of a set of numbers                              |
|                               |                                                                                                            |
|                               | where the geometric mean is preferred. It is a multiplicative factor, and so a                             |
|                               |                                                                                                            |
|                               | dimensionless quantity.                                                                                    |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| iqr                           | The interquartile range (IQR); It is the difference between the 75th and 25th                              |
|                               |                                                                                                            |
|                               | percentile of the data. It measures the dispersion similar to standard deviation                           |
|                               |                                                                                                            |
|                               | or variance but is much more robust against outliers.                                                      |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| entropy                       | The Shannon entropy                                                                                        |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| differential_entropy          | The differential entropy                                                                                   |
+-------------------------------+------------------------------------------------------------------------------------------------------------+
| MAD                           | The median absolute deviation (MAD) computes the median over the absolute                                  |
|                               |                                                                                                            |
|                               | deviations from the median. It is a measure of dispersion similar to the                                   |
|                               |                                                                                                            |
|                               | standard deviation but more robust to outliers.                                                            |
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





