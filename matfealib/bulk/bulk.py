
import numpy as np
import pandas as pd
from scipy import stats
import pymatgen
from tqdm.autonotebook import tqdm
# from tqdm import tqdm
from pymatgen.core.structure import IStructure
from pymatgen.analysis.local_env import (
    # BrunnerNNReal,
    # BrunnerNNReciprocal,
    # BrunnerNNRelative,
    # BrunnerNN_real,
    # BrunnerNN_reciprocal,
    # CovalentBondNN,
    # Critic2NN,
    CrystalNN,
    # CutOffDictNN,
    # EconNN,
    # IsayevNN,
    # JmolNN,
    # MinimumDistanceNN,
    # MinimumOKeeffeNN,
    # MinimumVIRENN,
    # NearNeighbors,
    # OpenBabelNN,
    # VoronoiNN,
)
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# import re
# from ..atomicfeatures.base import building_blocks
from pandas.api.types import is_numeric_dtype
# from pymatgen.core import Composition
from itertools import combinations


def func(inhomogeneous_list):
    tmp_list = []
    for i in inhomogeneous_list:
        if len(i[0]) == 1:
            tmp_list.append(i)
        else:
            for j in range(len(i[0])):
                tmp_list.append(([i[0][j]], [i[1][j]]))
    return tmp_list

def average_abs_deviation(lst):
    average = np.mean(lst)
    aad = np.mean(np.abs(np.subtract(lst, average)))
    return aad

def get_coordination_number(structure, idx='all'):
    nn_object = CrystalNN()
    tmp_structure = structure.get_primitive_structure()
    if idx == 'all':
        coordination_number_lst = []
        for i in range(tmp_structure.num_sites):
                tmp_coord = nn_object.get_cn(structure=tmp_structure,n=i)
                coordination_number_lst.append(tmp_coord)
        return coordination_number_lst
    else:
        tmp_coord = nn_object.get_cn(structure=tmp_structure,n=idx)
        return tmp_coord

def calc_avg_bond_angle(tmp_structure, idx):
    nn_object = CrystalNN()
    list_nn = nn_object.get_nn_info(structure=tmp_structure, n=idx)
    if not list_nn:
        return np.nan 
    else:
        tmp_coord_idx_lst = []
        for i in range(len(list_nn)):
            tmp_coord_idx_lst.append(list_nn[i]['site_index'])
            comb = combinations(tmp_coord_idx_lst, 2)
            angles = []
            for lst_idx in list(comb):
                selected_idxs = [ lst_idx[j] for j in range(len(lst_idx)) ]
                tmp_angle = tmp_structure.get_angle(selected_idxs[0],0,selected_idxs[1])
                angles.append(tmp_angle)
        return np.mean(angles)

def get_avg_bond_angle(structure):
    tmp_structure = structure.get_primitive_structure()
    avg_bond_ang_lst = []
    for i in range(tmp_structure.num_sites):
        tmp_value = calc_avg_bond_angle(tmp_structure, idx=i)
        if np.isnan(tmp_value):
            continue
        else:
            avg_bond_ang_lst.append(tmp_value)
    return avg_bond_ang_lst

def calc_bond_length(tmp_structure, idx, option):
    nn_object = CrystalNN()
    list_nn = nn_object.get_nn_info(structure=tmp_structure, n=idx)
    if not list_nn:
        return np.nan 
    else:
        dis_mat = tmp_structure.distance_matrix
        tmp_coord_idx_lst = []
        for i in range(len(list_nn)):
            tmp_coord_idx_lst.append(list_nn[i]['site_index'])
            lengths = []
            for coord_idx in tmp_coord_idx_lst:
                tmp_length = dis_mat[idx,coord_idx]
                lengths.append(tmp_length)
        if option == 'mean':
            return np.mean(lengths)
        if option == 'all':
            return lengths

def get_avg_bond_length(structure):
    tmp_structure = structure.get_primitive_structure()
    avg_bond_len_lst = []
    for i in range(tmp_structure.num_sites):
        tmp_value = calc_bond_length(tmp_structure, idx=i, option='mean')
        if np.isnan(tmp_value):
            continue
        else:
            avg_bond_len_lst.append(tmp_value)
    return avg_bond_len_lst

def get_packing_factor(structure):
    tmp_structure = structure.get_primitive_structure()
    avg_bond_len_lst = []
    for i in range(tmp_structure.num_sites):
        tmp_value = calc_bond_length(tmp_structure, idx=i, option='all')
        tmp_value_min = np.min(tmp_value)
        if np.isnan(tmp_value_min):
            continue
        else:
            avg_bond_len_lst.append(tmp_value_min)
    atomic_valume = 4/3*np.pi*(np.array(avg_bond_len_lst)/2)**3
    all_atom_valumes = atomic_valume.sum()
    packing_factor = all_atom_valumes / tmp_structure.volume
    return packing_factor

def get_lattice_system(structure):
    sga = SpacegroupAnalyzer(structure)
    crystal_system_str = sga.get_crystal_system()
    if crystal_system_str== 'triclinic':
        crystal_system = 1
    elif crystal_system_str== 'monoclinic':
        crystal_system = 2
    elif crystal_system_str== 'orthorhombic':
        crystal_system = 3
    elif crystal_system_str== 'tetragonal':
        crystal_system = 4
    elif crystal_system_str== 'trigonal':
        crystal_system = 5
    elif crystal_system_str== 'hexagonal':
        crystal_system = 6
    elif crystal_system_str== 'cubic':
        crystal_system = 7
    return crystal_system

def statistical_feature_values(compound,feature_name,statistical_functions='all'):

    column_names=[]
    fea_val = []

    if feature_name == 'packing_factor':
        fea_val.append(get_packing_factor(structure=compound))
        column_names.append(feature_name)
        return column_names, fea_val

    elif feature_name == 'number_of_sites':
        fea_val.append(compound.num_sites)
        column_names.append(feature_name)
        return column_names, fea_val

    elif feature_name == 'cell_volume':
        fea_val.append(compound.volume)
        column_names.append(feature_name)
        return column_names, fea_val

    elif feature_name == 'cell_density':
        fea_val.append(compound.density)
        column_names.append(feature_name)
        return column_names, fea_val

    elif feature_name == 'cell_volume_per_atom':
        tmp_cell_valume = compound.volume
        tmp_num_sites = compound.num_sites
        fea_val.append(tmp_cell_valume/tmp_num_sites)
        column_names.append(feature_name)
        return column_names, fea_val

    elif feature_name == 'crystal_system':
        fea_val.append(get_lattice_system(structure=compound))
        column_names.append(feature_name)
        return column_names, fea_val

    elif feature_name == 'space_group_number':
        sga = SpacegroupAnalyzer(structure=compound)
        fea_val.append(sga.get_space_group_number())
        column_names.append(feature_name)
        return column_names, fea_val

    elif feature_name == 'num_space_group_operations':
        sga = SpacegroupAnalyzer(structure=compound)
        fea_val.append(len(sga.get_space_group_operations()))
        column_names.append(feature_name)
        return column_names, fea_val

    elif feature_name == 'lattice_parameters':
        fea_val_lst=[]
        tmp_a = compound.lattice.a
        fea_val_lst.append(tmp_a)
        column_names.append('lattice_parameter_a')
        
        tmp_b = compound.lattice.b
        fea_val_lst.append(tmp_b)
        column_names.append('lattice_parameter_b')
        
        tmp_c = compound.lattice.c
        fea_val_lst.append(tmp_c)
        column_names.append('lattice_parameter_c')

        return column_names, fea_val_lst

    elif feature_name == 'lattice_angles':
        fea_val_lst=[]
        tmp_a = compound.lattice.alpha
        fea_val_lst.append(tmp_a)
        column_names.append('lattice_alpha')
        
        tmp_b = compound.lattice.beta
        fea_val_lst.append(tmp_b)
        column_names.append('lattice_beta')
        
        tmp_c = compound.lattice.gamma
        fea_val_lst.append(tmp_c)
        column_names.append('lattice_gamma')

        return column_names, fea_val_lst

    elif feature_name == 'coordination_number':
        stats_fea_vals = get_coordination_number(structure=compound)
        if len(stats_fea_vals)==0:          #
            print(compound.reduced_formula) #
            stats_fea_vals.append(np.nan)   #
        stats_fea_vals = np.array(stats_fea_vals)
    elif feature_name == 'average_bond_length':
        stats_fea_vals = get_avg_bond_length(structure=compound)
        if len(stats_fea_vals)==0:
            print(compound.reduced_formula)
            stats_fea_vals.append(np.nan)
        stats_fea_vals = np.array(stats_fea_vals)
    elif feature_name == 'average_bond_angle':
        stats_fea_vals = get_avg_bond_angle(structure=compound)
        if len(stats_fea_vals)==0:
            print(compound.reduced_formula)
            stats_fea_vals.append(np.nan)
        stats_fea_vals = np.array(stats_fea_vals)
    elif feature_name == 'distance_matrix':
        stats_fea_vals = compound.distance_matrix.flatten()
        stats_fea_vals = np.array(stats_fea_vals)

    else:
        raise ValueError("Your feature name is incorrect!!!")


    if (statistical_functions=='all'):
        min_value      = np.min(stats_fea_vals)
        max_value      = np.max(stats_fea_vals)
        sum_value      = np.sum(stats_fea_vals)
        mean_value     = np.mean(stats_fea_vals)
        std_value      = np.std(stats_fea_vals)
        var_value      = np.var(stats_fea_vals)
        median_value   = np.median(stats_fea_vals)
        diff_value     = max_value-min_value
        mode_value     = stats.mode(stats_fea_vals, keepdims=True).mode[0]
        gmean_value    = stats.gmean(stats_fea_vals)
        hmean_value    = stats.hmean(stats_fea_vals)
        pmean_value    = stats.pmean(stats_fea_vals,2)
        kur_value      = stats.kurtosis(stats_fea_vals)
        mom_value      = stats.moment(stats_fea_vals,3)
        expc_value     = stats.expectile(stats_fea_vals)
        skew_value     = stats.skew(stats_fea_vals)
        gstd_value     = stats.gstd(stats_fea_vals)
        iqr_value      = stats.iqr(stats_fea_vals)
        ent_value      = stats.entropy(stats_fea_vals)
        # diff_ent_value = stats.differential_entropy(stats_fea_vals)
        AAD_value      = average_abs_deviation(stats_fea_vals)
        MAD_value      = stats.median_abs_deviation(stats_fea_vals)

        tmp_dict={
            'min':min_value, 'max':max_value, 'sum':sum_value, 
            'diff':diff_value, 'mean':mean_value, 'mode': mode_value, 
            'std':std_value, 'median':median_value, 'var':var_value,
            'gmean':gmean_value, 'hmean':hmean_value, 'pmean': pmean_value,
            'kurtosis':kur_value, 'moment':mom_value, 'expectile':expc_value,
            'skew':skew_value, 'gstd':gstd_value, 'iqr':iqr_value, 
            'entropy':ent_value, 'AAD':AAD_value, 'MAD':MAD_value
        }
        
        for i in tmp_dict.keys():
            column_names.append(feature_name+'_{}'.format(i))
        return column_names, list(tmp_dict.values())
    
    elif isinstance(statistical_functions, list):
        tmp_lst=[]
        for i in statistical_functions:
            if i == 'min':
                min_value = np.min(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(min_value)
            if i == 'max':
                max_value = np.max(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(max_value)
            if i == 'sum':
                sum_value = np.sum(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(sum_value)
            if i == 'mean':
                mean_value = np.mean(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(mean_value)
            if i == 'std':
                std_value = np.std(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(std_value)
            if i == 'var':
                var_value = np.var(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(var_value)
            if i == 'median':
                median_value = np.median(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(median_value)
            if i == 'diff':
                diff_value = (np.max(stats_fea_vals)) - (np.min(stats_fea_vals))
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(diff_value)
            if i == 'mode':
                mode_value = stats.mode(stats_fea_vals, keepdims=True).mode[0]
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(mode_value)
            if i == 'gmean':
                gmean_value = stats.gmean(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(gmean_value)
            if i == 'hmean':
                hmean_value = stats.hmean(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(hmean_value)
            if i == 'pmean':
                pmean_value = stats.pmean(stats_fea_vals, 2)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(pmean_value)
            if i == 'kurtosis':
                kur_value = stats.kurtosis(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(kur_value)
            if i == 'moment':
                mom_value = stats.moment(stats_fea_vals, 3)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(mom_value)
            if i == 'expc':
                expc_value = stats.expectile(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(expc_value)
            if i == 'skew':
                skew_value = stats.skew(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(skew_value)
            if i == 'gstd':
                gstd_value = stats.gstd(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(gstd_value)
            if i == 'iqr':
                iqr_value = stats.iqr(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(iqr_value)
            if i == 'entropy':
                ent_value = stats.entropy(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(ent_value)
            if i == 'differential_entropy':
                diff_ent_value = stats.differential_entropy(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(diff_ent_value)
            if i == 'AAD':
                AAD_value = average_abs_deviation(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(AAD_value)
            if i == 'MAD':
                MAD_value = stats.median_abs_deviation(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(MAD_value)
                
        return column_names,tmp_lst
    
    elif (statistical_functions != 'all') and (isinstance(statistical_functions, str)):
        tmp_dict={
            'min', 'max', 'sum', 'diff', 'mode', 'mean', 'std', 'median', 'var', 
            'gmean', 'hmean', 'pmean', 'kurtosis', 'moment', 'expectile', 'skew', 
            'gstd', 'iqr', 'entropy', 'differential_entropy', 'AAD', 'MAD'
        }
        if statistical_functions not in tmp_dict:
            raise ValueError("The `statistical_functions` parameter "
                             "should be one of the `min`, `max`, `sum`, "
                             "`diff`, `mean`, `median` or `all` valuse")
        else:
            tmp_lst=[]
            if statistical_functions == 'min':
                min_value = np.min(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(min_value)
            if statistical_functions == 'max':
                max_value = np.max(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(max_value)
            if statistical_functions == 'sum':
                sum_value = np.sum(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(sum_value)
            if statistical_functions == 'mean':
                mean_value = np.mean(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(mean_value)
            if statistical_functions == 'std':
                std_value = np.std(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(std_value)
            if statistical_functions == 'var':
                var_value = np.var(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(var_value)
            if statistical_functions == 'median':
                median_value = np.median(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(median_value)
            if statistical_functions == 'diff':
                diff_value = (np.max(stats_fea_vals)) - (np.min(stats_fea_vals))
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(diff_value)
            if statistical_functions == 'mode':
                mode_value = stats.mode(stats_fea_vals, keepdims=True).mode[0]
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(mode_value) 
            if statistical_functions == 'gmean':
                gmean_value = stats.gmean(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(gmean_value)
            if statistical_functions == 'hmean':
                hmean_value = stats.hmean(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(hmean_value)
            if statistical_functions == 'pmean':
                pmean_value = stats.pmean(stats_fea_vals, 2)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(pmean_value)
            if statistical_functions == 'kurtosis':
                kur_value = stats.kurtosis(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(kur_value)
            if statistical_functions == 'moment':
                mom_value = stats.moment(stats_fea_vals, 3)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(mom_value)
            if statistical_functions == 'expectile':
                expc_value = stats.expectile(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(expc_value)
            if statistical_functions == 'skew':
                skew_value = stats.skew(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(skew_value)
            if statistical_functions == 'gstd':
                gstd_value = stats.gstd(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(gstd_value)
            if statistical_functions == 'iqr':
                iqr_value = stats.iqr(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(iqr_value)
            if statistical_functions == 'entropy':
                ent_value = stats.entropy(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(ent_value)
            if statistical_functions == 'differential_entropy':
                diff_ent_value = stats.differential_entropy(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(diff_ent_value)
            if statistical_functions == 'AAD':
                AAD_value = average_abs_deviation(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(AAD_value)
            if statistical_functions == 'MAD':
                MAD_value = stats.median_abs_deviation(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(MAD_value)

        return column_names,tmp_lst

def statistical_feature_values_df(
    dataframe_name,
    column_name,
    feature_name,
    statistical_functions='all'
    ):

    dataframe_name["Feature"] = dataframe_name[column_name].apply(
        statistical_feature_values,
        feature_name=feature_name,
        statistical_functions=statistical_functions
    )
    tmp_dataframe=pd.DataFrame(
        dataframe_name['Feature'].tolist(), 
        index=dataframe_name.index, 
        columns=['lst_col_names','lst_values']
    )
    tmp_col_names_lst=tmp_dataframe.lst_col_names.iloc[0]
    tmp_dataframe[tmp_col_names_lst] = pd.DataFrame(
        tmp_dataframe.lst_values.tolist(), 
        index= tmp_dataframe.index
    )
    dataframe_name=pd.concat([
        dataframe_name.drop('Feature', axis=1),
        tmp_dataframe.drop(['lst_col_names','lst_values'], axis=1)
        ], axis=1
    )

    return dataframe_name


def statistical_features(
    compound,
    feature='all',
    statistical_functions='all'
    ):

    if (feature=='all'):
        tmp_all_list=[]
        fea_collection_keys_list = [
            'packing_factor', 
            'number_of_sites', 
            'cell_volume', 
            'cell_density', 
            'cell_volume_per_atom', 
            'crystal_system', 
            'space_group_number', 
            'num_space_group_operations',
            'lattice_parameters',
            'lattice_angles',
            'distance_matrix',
            'coordination_number',
            'average_bond_length',
            'average_bond_angle'
        ]
        for i in range(len( fea_collection_keys_list )):
            # if is_numeric_dtype(feature_collection[fea_collection_keys_list[i]])==True:
            tmp_all_list.append(
                statistical_feature_values(
                    compound,
                    feature_name=fea_collection_keys_list[i],
                    statistical_functions=statistical_functions
                )
            )
        return tmp_all_list

    elif isinstance(feature, list):
        tmp_list=[]
        for i in range(len(feature)):
            tmp_list.append(
                statistical_feature_values(
                    compound,
                    feature_name=feature[i],
                    statistical_functions=statistical_functions
                )
            )
        return tmp_list

    elif feature != 'all' and isinstance(feature, str):
        return statistical_feature_values(
            compound,
            feature_name=feature,
            statistical_functions=statistical_functions
        )
    #     return type(arg)
    # if isinstance(arg, pymatgen.core.composition.Composition):
    #     return type(arg)
    # else:
        # return "Not a dataframe"


def statistical_features_df(
    dataframe_name,
    column_name, 
    feature='all',
    statistical_functions='all'
    ):
    
    if (feature=='all'):
        fea_collection_keys_list = [
            'packing_factor', 
            'number_of_sites', 
            'cell_volume', 
            'cell_density', 
            'cell_volume_per_atom', 
            'crystal_system', 
            'space_group_number', 
            'num_space_group_operations',
            'lattice_parameters',
            'lattice_angles',
            'distance_matrix',
            'coordination_number',
            'average_bond_length',
            'average_bond_angle'
        ]
        for i in tqdm(
            range(len(fea_collection_keys_list)), 
            bar_format='{l_bar}{bar}| [{elapsed}<{remaining}, ' '{rate_fmt}{postfix}]', 
            desc="Task in progress"
            ):
            # if is_numeric_dtype(feature_collection[fea_collection_keys_list[i]])==True:
            dataframe_name = statistical_feature_values_df(
                dataframe_name,
                column_name,
                feature_name=(fea_collection_keys_list[i]),
                statistical_functions=statistical_functions
            )
        return dataframe_name

    elif isinstance(feature, list):
        tmp_list=[]
        for i in tqdm(
            range(len(feature)), 
            bar_format='{l_bar}{bar}| [{elapsed}<{remaining}, ' '{rate_fmt}{postfix}]', 
            desc="Task in progress"
            ):
            dataframe_name = statistical_feature_values_df(
                dataframe_name,
                column_name,
                feature_name=feature[i],
                statistical_functions=statistical_functions
            )
        return dataframe_name

    elif feature != 'all' and isinstance(feature, str):
        return statistical_feature_values_df(
            dataframe_name,
            column_name,
            feature_name=feature,
            statistical_functions=statistical_functions
        )
    #     return type(arg)
    # if isinstance(arg, pymatgen.core.composition.Composition):
    #     return type(arg)
    # else:
        # return "Not a dataframe"


def fetch_bulk_features(
    structures, 
    features='all', 
    column_name=None, 
    statistical_functions='all'
    ):

    tmp_dict={
        'min', 'max', 'sum', 'diff', 'mode', 'mean', 'std', 'median', 'var', 
        'gmean', 'hmean', 'pmean', 'kurtosis', 'moment', 'expectile', 'skew', 
        'gstd', 'iqr', 'entropy', 'differential_entropy', 'AAD', 'MAD'
    }
    msg = ("invalid statistical function `{}`. The `statistical_functions` "
           "parameter should be 'all' or from the {} values.")

    if (statistical_functions != 'all') and (isinstance(statistical_functions, str)):
        if statistical_functions not in tmp_dict:
            raise ValueError(msg.format(statistical_functions, tmp_dict))
    if (statistical_functions != 'all') and isinstance(statistical_functions, list):
        for i in statistical_functions:
            if i not in tmp_dict:
                raise ValueError(msg.format(i, tmp_dict))

    if isinstance(structures, pymatgen.core.structure.IStructure):
        if features !='all' and isinstance(features, str):
            values= [statistical_features(structures,features,statistical_functions)[1]]
            names = statistical_features(structures,features,statistical_functions)[0]
            return pd.DataFrame(values,columns=names,index=[structures.reduced_formula])
        else :
            tmp_array=np.array(func(statistical_features(structures,features,statistical_functions)))
            names=tmp_array[:,0].flatten()
            values=[tmp_array[:,1].flatten()]
            return pd.DataFrame(values,columns=names,index=[structures.reduced_formula])
    if isinstance(structures, list):
        tmp_df=pd.DataFrame(structures,columns=["formula"])
        return statistical_features_df(tmp_df,"formula",features,statistical_functions)
    if isinstance(structures, pd.DataFrame):
        tmp_dataframe_name=structures.copy(deep=True)
        if (column_name==None):
            raise ValueError("The input is `pd.DataFrame` and `column_name` argument is not given. Please inter materials column name.")
        else :
            return statistical_features_df(tmp_dataframe_name,column_name,features,statistical_functions=statistical_functions)
