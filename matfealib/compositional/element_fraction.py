from matfealib.atomicfeatures.base import building_blocks
import pandas as pd
import numpy as np

symbols = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg',
          'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr',
          'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br',
          'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd',
          'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La',
          'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er',
          'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au',
          'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
          'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md',
          'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn',
          'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']

def element_fraction(compound: str) -> list:
    """Function for create element fraction.

    This function create element fraction vector for a given 
    chemical formula.

    Parameters
    ----------
    compound : str
        Chemical formula of material

    Returns
    -------
    list
        element fraction vector 

    """
    fraction_lst = [0] * len(symbols)
    element, stochiometry = building_blocks(compound)
    for i in range(len(stochiometry)):
        subscripts_sum = sum(stochiometry)
        fraction = (stochiometry[i] / subscripts_sum)
        for j in range(len(symbols)):
            if (element[i] == symbols[j]):
                fraction_lst[j] = fraction
    return fraction_lst

def element_fraction_df(
    dataframe: pd.DataFrame,
    column_name: str,
) -> pd.DataFrame:
    """Function for create element fraction.

    This function create element fraction vector for a given
    pd.DataFrame.

    Parameters
    ----------
    compound : str
        Chemical formula of material
    column_name: str
        Column's name of materials chemical formula

    Returns
    -------
    pd.DataFrame
        Element fraction of materials in the form of a pd.DataFrame

    """
    fraction = dataframe[column_name].apply(element_fraction)
    fraction_df = pd.DataFrame(
        fraction.to_list(),
        columns = symbols,
        index = dataframe.index.values,
        dtype = 'float'
    )
    return pd.concat([dataframe, fraction_df], axis=1)

def fetch_element_fraction(
    compound, 
    column_name : str = None
) -> pd.DataFrame:
    """Function for create element fraction.

    This function create element fraction vector for (a) given 
    material(s), in the form of a single string, list or pd.DataFrame

    Parameters
    ----------
    compound
        Chemical formula of material(s)
    column_name : str, default=None

    Returns
    -------
    pd.DataFrame
        Element fraction of material(s) in the form of a pd.DataFrame

    """
    if isinstance(compound, str):
        fraction = element_fraction(compound)
        return pd.DataFrame([fraction], columns=symbols, index=[compound])
    if isinstance(compound, list):
        tmp_df = pd.DataFrame(compound, columns=["formula"])
        return element_fraction_df(tmp_df, 'formula')
    if isinstance(compound, pd.DataFrame):
        # tmp_dataframe_name=compounds.copy(deep=True)
        if (column_name == None):
            raise ValueError('The input is `pd.DataFrame` and '
                             '`column_name` argument is not given. '
                             'Please inter materials column name.')
        else:
            return element_fraction_df(compound, column_name)
