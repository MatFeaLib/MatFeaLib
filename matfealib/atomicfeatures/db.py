
import pandas as pd
import numpy as np
import os
from collections import OrderedDict

module_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(module_dir, "..", "data")

files = os.listdir(data_dir)

pathfiles=[]
for i in range(len(files)):
    pathfiles.append(os.path.join(data_dir,"{}".format(files[i]),"elemental_features.csv"))

def GetFunction(row,column_name,ist=0):
    try:
        tmp_dict=row[column_name]
        if pd.isna(tmp_dict)==False:
            tmp_key=list(eval(tmp_dict).keys())[ist]
            return eval(tmp_dict)[tmp_key]
    except IndexError as e:
        # print("Error on sample",row.name,'---> There are some problems for values in this sample. By default we return `None` value as feature', '(The error is:',e,')')
        return None

# def GetOxidationStates(row,column_name,ist=0):                                                          ### we drop oxidation_states values
#     try:
#         tmp_list=row[column_name]
#         if (not tmp_list) == False :
#             return eval(tmp_list)[ist]
#     except IndexError as e:
#         # print("Error on atom",row.name,row.chemical_symbol,'---> There are some problems for feature values in this sample. By default MatFeaLib return `None` value as feature', '(The error is:',e,')')
#         return None

def GetOrbitalElectrons(row,column_name,orbital_name):
    try:
        tmp_oddict=row[column_name]
        # print(row.name,tmp_oddict)
        if pd.isna(tmp_oddict)==False:
            tmp_key_list=list(eval(tmp_oddict).keys())
            sum_of_electrons=0
            for i in tmp_key_list:
                if i[1]==orbital_name:
                    tmp_key=i
                    tmp_value=eval(tmp_oddict)[tmp_key]
                    sum_of_electrons+=tmp_value
                # print(sum_of_electrons)
            return sum_of_electrons
        elif pd.isna(tmp_oddict):
            return None
    except IndexError as e:
        print("Warning on atom",row.name, row.chemical_symbol,'---> There are some problems for feature value(s) in this sample. By default we return `None` value as feature', '(The error is:',e,')')
        return None

def GetLastSubshell(row,column_name):
    try:
        tmp_tuple=row[column_name]
        if (not tmp_tuple) == False :
            return eval(tmp_tuple)[1]
    except IndexError as e:
        print("Error on atom",row.name,row.chemical_symbol,'---> There are some problems for feature values in this sample. By default MatFeaLib return `None` value as feature', '(The error is:',e,')')
        return None

#-------------------------
def GetPymatgenOxidationStates(row,column_name,ist=0):
    try:
        tmp_list=row[column_name]
        if (tmp_list is not np.nan):
            if ((not tmp_list) == False):
                return eval(tmp_list)[ist]
    except IndexError as e:
        # print("Error on atom",row.name,row.chemical_symbol,'---> There are some problems for feature values in this sample. By default MatFeaLib return `None` value as feature', '(The error is:',e,')')
        return None

def GetPymatgenIonizationEnergy(row,column_name,ist=0):
    try:
        tmp_list=row[column_name]
        if (not tmp_list) == False :
            return eval(tmp_list)[ist]
    except IndexError as e:
        # print("Error on atom",row.name,row.chemical_symbol,'---> There are some problems for feature values in this sample. By default MatFeaLib return `None` value as feature', '(The error is:',e,')')
        return None

def GetMeltingPoint(row,column_name,ist=0):
    tmp_list=row[column_name]
    if tmp_list is not np.nan:
        try:
            return eval(tmp_list)
        except SyntaxError as e:
            return None
    else:
        return None
#-------------------------

#data=[]
#for f, v in zip(pathfiles,files):
#    df = pd.read_csv(f, index_col=0)
#    globals()[v]=df
data=[]
for f, v in zip(pathfiles,files):
    df = pd.read_csv(f, index_col=0)

    if v=='mendeleev':
        df['ionization_energy'] = df.apply(GetFunction, axis=1, column_name='ionization_energy')
        # df['oxidation_states'] = df.apply(GetOxidationStates, axis=1, column_name='oxidation_states')   ### we drop oxidation_states values
        df['screening_constant'] = df.apply(GetFunction, axis=1, column_name='screening_constant')
        df['number_of_s_electrons'] = df.apply(GetOrbitalElectrons, axis=1, column_name='electron_configuration', orbital_name='s')
        df['number_of_p_electrons'] = df.apply(GetOrbitalElectrons, axis=1, column_name='electron_configuration', orbital_name='p')
        df['number_of_d_electrons'] = df.apply(GetOrbitalElectrons, axis=1, column_name='electron_configuration', orbital_name='d')
        df['number_of_f_electrons'] = df.apply(GetOrbitalElectrons, axis=1, column_name='electron_configuration', orbital_name='f')
        df['electrons_per_shell'] = df.apply(GetFunction, axis=1, column_name='electrons_per_shell')
        df['last_subshell'] = df.apply(GetLastSubshell, axis=1, column_name='last_subshell')
        df.drop([
            'spin_occupations',
            'oxides', 
            'description', 
            'electronic_configuration', 
            'lattice_structure', 
            'chemical_name', 
            'electronegativity_li-xue',
            'oxidation_states',                                                                           ### we drop oxidation_states values
            'electron_configuration'
        ], axis=1, inplace=True)
        # df.max_l.replace({'s':0, 'p':1,'d':2},inplace=True)
        pd.set_option('future.no_silent_downcasting', True)
        df['max_l'] = df['max_l'].replace({'s':0, 'p':1,'d':2}).astype(int)
        # df.block_periodic_table.replace({'s':0, 'p':1,'d':2, 'f':3},inplace=True)
        df['block_periodic_table'] = df['block_periodic_table'].replace({'s':0, 'p':1,'d':2, 'f':3}).astype(int)

    if v=='pymatgen':
        df['orbitals_energy'] = df.apply(GetFunction, axis=1, column_name='orbitals_energy')
        df['common_oxidation_states'] = df.apply(GetPymatgenOxidationStates, axis=1, column_name='common_oxidation_states')
        df['ionic_radius'] = df.apply(GetFunction, axis=1, column_name='ionic_radius')
        df['melting_point'] = df.apply(GetMeltingPoint, axis=1, column_name='melting_point')
        df['oxidation_states'] = df.apply(GetPymatgenOxidationStates, axis=1, column_name='oxidation_states')
        df['ICSD_oxidation_states'] = df.apply(GetPymatgenOxidationStates, axis=1, column_name='ICSD_oxidation_states')
        df['ionization_energy'] = df.apply(GetPymatgenIonizationEnergy, axis=1, column_name='ionization_energy')
        df.drop([
            'electrical_resistivity',
            'electron_configuration', 
            'hardness_mineral', 
            'chemical_name', 
            'refractive_index', 
            'atomic_radius_shannon', 
            'superconduction_temperature',
            'NMR_quadrupole_moment',
        ], axis=1, inplace=True)

    globals()[v]=df


def available_collection():
    """
    Return a dataframe with available data collections and corresponding definition.

    Parameters
    ----------
    None

    Returns
    -------
    pandas.DataFrame
    """
    
    lst=[]
    lst.append(files)
    description=[]
    for i in range (len(files)):
        with open(os.path.join(data_dir,"{}".format(files[i]),"README.txt")) as f:
            lines = f.readlines()
            description.append(lines[0].rstrip())
    lst.append(description)
    df = pd.DataFrame(lst).transpose()
    df.columns=['Collection','Description']
    df.sort_values("Collection",inplace=True)
    df.index = np.arange(1, len(df)+1)
    pd.set_option("display.max_colwidth", None)
    df_ = df.style.set_table_styles([dict(selector = 'th', props=[('text-align', 'left')])])
    df_.set_properties(**{'text-align': 'left'})
    return df_

def available_features(feature_collection):
    """
    Return available features within a feature collection.

    Parameters
    ----------
    feature_collection : feature collection name

    Returns
    -------
    
    """

    return feature_collection.keys()

