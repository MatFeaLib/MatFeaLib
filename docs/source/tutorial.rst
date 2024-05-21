
Tutorial
========

The available atomic feature collections in MatFeaLib package can be assess via:

.. code-block:: python

   available_collection()

For each collection, the following function displays the containing features within a collection:

.. code-block:: python

   available_features("collection name")

The ``fetch_elemental_features`` method returns atomic features for a single material or a set of multiple materials. 
For a single string:

.. code-block:: python
   
   fetch_elemental_features(string, collection="collection name", features='all')

For a list of materials:

.. code-block:: python

   fetch_elemental_features(list, collection="collection name", features='all')

For a DataFrame of samples:

.. code-block:: python
   
   fetch_elemental_features(dataframe, 
                            column_name="column name", 
                            collection="collection name", 
                            features='all')

The ``fetch_statistical_features`` method returns statistical features of a given material, list of materials, or a dataframe:

.. code-block:: python

   fetch_statistical_features(compound(s), collection="collection name", features='all')



