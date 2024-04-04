
import numpy as np
import pandas as pd
# import re
from .base import building_blocks
from pandas.api.types import is_numeric_dtype

def statistical_feature_values(compound,feature_collection,feature_name,statistical_functions='all'):

    column_names=[]
    atoms = building_blocks(compound,'element')
    stats_fea_vals=[]
    for atom in atoms:
        tmp_val = feature_collection.loc[feature_collection['chemical_symbol'] == atom][feature_name].values
        stats_fea_vals.append(tmp_val[0])

    stats_fea_vals_array = np.array(stats_fea_vals)

    min_value    = stats_fea_vals_array.min()
    max_value    = stats_fea_vals_array.max()
    sum_value    = stats_fea_vals_array.sum()
    diff_value   = min_value=max_value-min_value
    mean_value   = stats_fea_vals_array.mean()
    std_value    = stats_fea_vals_array.std()
    # median_value = stat_fea_vals_array.median()

    tmp_dict={'min':min_value, 'max':max_value, 'sum':sum_value, 'diff':diff_value, 'mean':mean_value, 'std':std_value}

    if (statistical_functions=='all'):
        for i in tmp_dict.keys():
            column_names.append(feature_name+'_{}'.format(i))
        return column_names, list(tmp_dict.values())
    elif isinstance(statistical_functions, list):
        tmp_lst=[]
        for i in statistical_functions:
            column_names.append(feature_name+'_{}'.format(i))
            tmp_lst.append(tmp_dict[i])
        return column_names,tmp_lst
    elif statistical_functions != 'all' and isinstance(statistical_functions, str):
        if statistical_functions not in tmp_dict.keys():
            raise ValueError("The `statistical_functions` parameter should be one of the `min`, `max`, `sum`, `diff`, `mean`, `median` or `all` valuse")
        else:
            tmp_lst=[]
            column_names.append(feature_name+'_{}'.format(statistical_functions))
            tmp_lst.append(tmp_dict[statistical_functions])
            return column_names,tmp_lst

def statistical_feature_values_df(dataframe_name,column_name,feature_collection,feature_name,statistical_functions='all'):

    dataframe_name["Feature"]=dataframe_name[column_name].apply(statistical_feature_values,feature_collection=feature_collection,feature_name=feature_name,statistical_functions=statistical_functions)
    tmp_dataframe=pd.DataFrame(dataframe_name['Feature'].tolist(), index=dataframe_name.index, columns=['lst_col_names','lst_values'])
    tmp_col_names_lst=tmp_dataframe.lst_col_names[0]
    tmp_dataframe[tmp_col_names_lst] = pd.DataFrame(tmp_dataframe.lst_values.tolist(), index= tmp_dataframe.index)
    dataframe_name=pd.concat([dataframe_name.drop('Feature',axis=1),tmp_dataframe.drop(['lst_col_names','lst_values'],axis=1)],axis=1)

    return dataframe_name


def statistical_features(compound,feature_collection,feature='all',statistical_functions='all'):

    if (feature=='all'):
        tmp_all_list=[]
        fea_collection_keys_list=feature_collection.keys()
        for i in range(len( fea_collection_keys_list )):
            if is_numeric_dtype(feature_collection[fea_collection_keys_list[i]])==True:
                tmp_all_list.append(statistical_feature_values(compound,feature_collection,feature_name=fea_collection_keys_list[i],statistical_functions=statistical_functions))
        return tmp_all_list
    elif isinstance(feature, list):
        tmp_list=[]
        for i in range(len(feature)):
            tmp_list.append(statistical_feature_values(compound,feature_collection,feature_name=feature[i],statistical_functions=statistical_functions))
        return tmp_list
    elif feature != 'all' and isinstance(feature, str):
        return statistical_feature_values(compound,feature_collection,feature_name=feature,statistical_functions=statistical_functions)
    #     return type(arg)
    # if isinstance(arg, pymatgen.core.composition.Composition):
    #     return type(arg)
    # else:
        # return "Not a dataframe"


def statistical_features_df(dataframe_name,column_name,feature_collection,feature='all',statistical_functions='all'):
    
    if (feature=='all'):
        fea_collection_keys_list=feature_collection.keys()
        for i in range(len( fea_collection_keys_list )):
            if is_numeric_dtype(feature_collection[fea_collection_keys_list[i]])==True:
                dataframe_name=statistical_feature_values_df(dataframe_name,column_name,feature_collection,feature_name=(fea_collection_keys_list[i]),statistical_functions=statistical_functions)
        return dataframe_name
    elif isinstance(feature, list):
        tmp_list=[]
        for i in range(len(feature)):
            dataframe_name=statistical_feature_values_df(dataframe_name,column_name,feature_collection,feature_name=feature[i],statistical_functions=statistical_functions)
        return dataframe_name
    elif feature != 'all' and isinstance(feature, str):
        return statistical_feature_values_df(dataframe_name,column_name,feature_collection,feature_name=feature,statistical_functions=statistical_functions)
    #     return type(arg)
    # if isinstance(arg, pymatgen.core.composition.Composition):
    #     return type(arg)
    # else:
        # return "Not a dataframe"


def fetch_statistical_features(compounds, collection, features='all', column_name=None, statistical_functions='all'):
    if isinstance(compounds, str):
        if features !='all' and isinstance(features, str):
            values= [statistical_features(compounds,collection,features,statistical_functions)[1]]
            names = statistical_features(compounds,collection,features,statistical_functions)[0]
            return pd.DataFrame(values,columns=names,index=[compounds])
        else :
            n_features=len(statistical_features(compounds,collection,features,statistical_functions))
            n_elements=len(statistical_features(compounds,collection,features,statistical_functions)[0][0])
            tmp_array=np.array(statistical_features(compounds,collection,features,statistical_functions))
            names=list(tmp_array[:,0].reshape(1,n_features*n_elements)[0])
            values=tmp_array[:,1].reshape(1,n_features*n_elements)
            return pd.DataFrame(values,columns=names,index=[compounds])
    if isinstance(compounds, list):
        tmp_df=pd.DataFrame(compounds,columns=["formula"])
        return statistical_features_df(tmp_df,"formula",collection,features,statistical_functions)
    if isinstance(compounds, pd.DataFrame):
        tmp_dataframe_name=compounds.copy(deep=True)
        if (column_name==None):
            raise ValueError("The input is `pd.DataFrame` and `column_name` argument is not given. Please inter materials column name.")
        else :
            return statistical_features_df(tmp_dataframe_name,column_name,collection,features,statistical_functions=statistical_functions)

