
import numpy as np
import pandas as pd
from scipy import stats
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

    if (statistical_functions=='all'):
        min_value      = np.min(stats_fea_vals)
        max_value      = np.max(stats_fea_vals)
        sum_value      = np.sum(stats_fea_vals)
        mean_value     = np.mean(stats_fea_vals)
        std_value      = np.std(stats_fea_vals)
        var_value      = np.var(stats_fea_vals)
        median_value   = np.median(stats_fea_vals)
        diff_value     = max_value-min_value
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
        MAD_value      = stats.median_abs_deviation(stats_fea_vals)

        tmp_dict={'min':min_value, 'max':max_value, 'sum':sum_value, 
                  'diff':diff_value, 'mean':mean_value, 'std':std_value, 
                  'median':median_value, 'var':var_value, 'gmean':gmean_value, 
                  'hmean':hmean_value, 'pmean': pmean_value, 'kurtosis':kur_value, 
                  'moment':mom_value, 'expectile':expc_value, 'skew':skew_value, 
                  'gstd':gstd_value, 'iqr':iqr_value, 'entropy':ent_value, 
                  'MAD':MAD_value}
        
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
            if i == 'MAD':
                MAD_value = stats.median_abs_deviation(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(i))
                tmp_lst.append(MAD_value)
                
        return column_names,tmp_lst
    
    elif statistical_functions != 'all' and isinstance(statistical_functions, str):
        tmp_dict={'min', 'max', 'sum', 'diff', 'mean', 'std', 'median', 'var', 
                  'gmean', 'hmean', 'pmean', 'kurtosis', 'moment', 'expectile', 
                  'skew', 'gstd', 'iqr', 'entropy', 'differential_entropy', 'MAD'}
        if statistical_functions not in tmp_dict:
            raise ValueError("The `statistical_functions` parameter should be one of the `min`, `max`, `sum`, `diff`, `mean`, `median` or `all` valuse")
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
            if statistical_functions == 'MAD':
                MAD_value = stats.median_abs_deviation(stats_fea_vals)
                column_names.append(feature_name+'_{}'.format(statistical_functions))
                tmp_lst.append(MAD_value)

        return column_names,tmp_lst

def statistical_feature_values_df(dataframe_name,column_name,feature_collection,feature_name,statistical_functions='all'):

    dataframe_name["Feature"]=dataframe_name[column_name].apply(statistical_feature_values,feature_collection=feature_collection,feature_name=feature_name,statistical_functions=statistical_functions)
    tmp_dataframe=pd.DataFrame(dataframe_name['Feature'].tolist(), index=dataframe_name.index, columns=['lst_col_names','lst_values'])
    tmp_col_names_lst=tmp_dataframe.lst_col_names.iloc[0]
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

