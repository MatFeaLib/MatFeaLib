
import numpy as np
import pandas as pd
# import re

from .base import building_blocks

def get_feature_values(compound,feature_collection,feature_name):
    """
    Return feature values for a given chemical formula.
    """

    column_names=[]
    atoms = building_blocks(compound,'element')
    for idx in range(len(atoms)):
        column_names.append('{}_{}_{}'.format(feature_name,idx+1,atoms[idx]))
    mat_fea_vals=[]
    for atom in atoms:
        tmp_val = feature_collection.loc[feature_collection['chemical_symbol'] == atom][feature_name].values
        mat_fea_vals.append(tmp_val[0])

    return column_names, mat_fea_vals

def get_feature_values_df(dataframe_name,column_name,feature_collection,feature_name):

    dataframe_name["Feature"]=dataframe_name[column_name].apply(get_feature_values,feature_collection=feature_collection,feature_name=feature_name)
    dataframe_name["Elements"]=dataframe_name[column_name].apply(building_blocks,option='element')
    dataframe_name["Number_of_Elements"]=dataframe_name["Elements"].apply(len)
    # unique_elements = dataframe_name["Number_of_Elements"].unique()
    max_n_elements = dataframe_name["Number_of_Elements"].max()
    column_names=[]
    for i in range(max_n_elements):
        column_names.append('{}_{}'.format(feature_name,i+1))
    pd.concat([dataframe_name,pd.DataFrame(columns=column_names)])
    for i in range(len(dataframe_name)):
        for j in range(dataframe_name.Number_of_Elements.iloc[i]):
            dataframe_name.loc[dataframe_name.index[i],column_names[j]]=(dataframe_name['Feature']).iloc[i][1][j]
    
    return dataframe_name.drop(["Feature","Elements","Number_of_Elements"],axis=1)

# # 4 Bahman 2024 - 22:13
# def get_feature_values_df(dataframe_name,column_name,feature_collection,feature_name):

#     df=dataframe_name.copy(deep=True)
#     df["Feature"]=df[column_name].apply(get_feature_values,feature_collection=feature_collection,feature_name=feature_name)
#     df["Elements"]=df[column_name].apply(building_blocks,option='element')
#     df["Number_of_Elements"]=df["Elements"].apply(len)
#     # unique_elements = df["Number_of_Elements"].unique()
#     max_n_elements = df["Number_of_Elements"].max()
#     column_names=[]
#     for i in range(max_n_elements):
#         column_names.append('{}_{}'.format(feature_name,i+1))
#     pd.concat([df,pd.DataFrame(columns=column_names)])
#     for i in range(len(df)):
#         for j in range(df.Number_of_Elements.iloc[i]):
#             df.loc[df.index[i],column_names[j]]=(df['Feature'])[i][1][j]
    
#     return df.drop(["Feature","Elements","Number_of_Elements"],axis=1)



def get_features(compound,feature_collection,feature='all'):

    if (feature=='all'):
        tmp_all_list=[]
        for i in range(len(feature_collection.keys())):
            tmp_all_list.append(get_feature_values(compound,feature_collection,feature_name=(feature_collection.keys())[i]))
        return tmp_all_list
    elif isinstance(feature, list):
        tmp_list=[]
        for i in range(len(feature)):
            tmp_list.append(get_feature_values(compound,feature_collection,feature_name=feature[i]))
        return tmp_list
    elif feature != 'all' and isinstance(feature, str):
        return get_feature_values(compound,feature_collection,feature_name=feature)
    #     return type(arg)
    # if isinstance(arg, pymatgen.core.composition.Composition):
    #     return type(arg)
    # else:
        # return "Not a dataframe"


def get_features_df(dataframe_name,column_name,feature_collection,feature='all'):
    if (feature=='all'):
        for i in range(len(feature_collection.keys())):
            tmp_all_df=get_feature_values_df(dataframe_name,column_name,feature_collection,feature_name=(feature_collection.keys())[i])
        return tmp_all_df
    elif isinstance(feature, list):
        tmp_list=[]
        for i in range(len(feature)):
            tmp_list_df=get_feature_values_df(dataframe_name,column_name,feature_collection,feature_name=feature[i])
        return tmp_list_df
    elif feature != 'all' and isinstance(feature, str):
        return get_feature_values_df(dataframe_name,column_name,feature_collection,feature_name=feature)
    #     return type(arg)
    # if isinstance(arg, pymatgen.core.composition.Composition):
    #     return type(arg)
    # else:
        # return "Not a dataframe"


# def fetch_features(compounds, collection, features='all', column_name=None):
#     if isinstance(compounds, str):
#         # return get_features(compounds,collection,features)
#         if features !='all' and isinstance(features, str):
#             values= [get_features(compounds,collection,features)[1]]
#             names = get_features(compounds,collection,features)[0]
#             return pd.DataFrame(values,columns=names,index=[compounds])
#         else :
#             n_features=len(get_features(compounds,collection,features))
#             n_elements=len(get_features(compounds,collection,features)[0][0])
#             tmp_array=np.array(get_features(compounds,collection,features))
#             names=list(tmp_array[:,0].reshape(1,n_features*n_elements)[0])
#             values=tmp_array[:,1].reshape(1,n_features*n_elements)
#             return pd.DataFrame(values,columns=names,index=[compounds])
#     if isinstance(compounds, list):
#         tmp_df=pd.DataFrame(compounds,columns=["formula"])
#         # return tmp_df
#         return get_features_df(tmp_df,"formula",collection,features)
#     if isinstance(compounds, pd.DataFrame):
#         if (column_name==None):
#             raise ValueError("The input is `pd.DataFrame` and `column_name` argument is not given. Please inter materials column name.")
#         else :
#             return get_features_df(compounds,column_name,collection,features)

# Jan 25, 2024 - 13:00
def fetch_elemental_features(compounds, collection, features='all', column_name=None):
    if isinstance(compounds, str):
        # return get_features(compounds,collection,features)
        if features !='all' and isinstance(features, str):
            values= [get_features(compounds,collection,features)[1]]
            names = get_features(compounds,collection,features)[0]
            return pd.DataFrame(values,columns=names,index=[compounds])
        else :
            n_features=len(get_features(compounds,collection,features))
            n_elements=len(get_features(compounds,collection,features)[0][0])
            tmp_array=np.array(get_features(compounds,collection,features))
            names=list(tmp_array[:,0].reshape(1,n_features*n_elements)[0])
            values=tmp_array[:,1].reshape(1,n_features*n_elements)
            return pd.DataFrame(values,columns=names,index=[compounds])
    if isinstance(compounds, list):
        tmp_df=pd.DataFrame(compounds,columns=["formula"])
        # return tmp_df
        return get_features_df(tmp_df,"formula",collection,features)
    if isinstance(compounds, pd.DataFrame):
        tmp_dataframe_name=compounds.copy(deep=True)
        if (column_name==None):
            raise ValueError("The input is `pd.DataFrame` and `column_name` argument is not given. Please inter materials column name.")
        else :
            return get_features_df(tmp_dataframe_name,column_name,collection,features)





