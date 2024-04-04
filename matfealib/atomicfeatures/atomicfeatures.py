import numpy as np
import pandas as pd
import re
import os

module_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(module_dir, "..", "data")

files = os.listdir(data_dir)

pathfiles=[]
for i in range(len(files)):
    pathfiles.append(os.path.join(data_dir,"{}".format(files[i]),"elemental_features.csv"))

data=[]
for f, v in zip(pathfiles,files):
    df = pd.read_csv(f, index_col=0)
    globals()[v]=df


def available_collection():
    lst=[]
    lst.append(files)
    description=[]
    for i in range (len(files)):
        with open(os.path.join(data_dir,"{}".format(files[i]),"README.txt")) as f:
            lines = f.readlines()
            description.append(lines[0].rstrip())
    lst.append(description)
    df = pd.DataFrame(lst).transpose()
    df.columns=['collection','description']
    pd.set_option("display.max_colwidth", None)
#    df = df.style.set_properties(**{'text-align': 'left'})
#    df = df.set_table_styles([dict(selector = 'th', props=[('text-align', 'left')])])
    return df

def available_features(feature_collection):
    return feature_collection.keys()

def refine_chem_formula(compound):
    # print('old: ',compound)
    if '(' in compound:
        parts   = re.findall(r'\(.*?\)', compound)             # Obtain Paranthesis "(string)"
        numbers = re.findall(r'\).*?([\d\.]+).*?', compound)   # Obtain Number after paranthesis
        new_text= re.sub(r'\).*?([\d\.]+).*?',")", compound)   # Remove Number after paranthesis

        comp=[]
        c=0
        for i in parts:
            elements_lst=[]
            stoichiometry_lst=[]
            tmp_elem_lst=re.findall('[A-Z][^A-Z]*', i)         # Obtain different parts
            for j in tmp_elem_lst:
                elements_lst.append(re.findall('(\d+|[A-Za-z]+)', j)[0])
                if len(re.findall('(\d+|[A-Za-z]+)', j))==1:
                    stoichiometry_lst.append( 1*eval(numbers[c]) )
                else:
                    stoichiometry_lst.append( eval(re.findall(r"[-+]?(?:\d*\.*\d+)", i)[0])* eval(numbers[c]) )
            c+=1
            new_list = [f"{item1}{item2}" for item1, item2 in zip(elements_lst, stoichiometry_lst)]
            new_string = '('+''.join(new_list)+')'
            comp.append(new_string)                            # new paranthesis 

        for i in range(len(parts)):
            new_text=new_text.replace(parts[i], comp[i])       # replace paranthesis by new strings

        new_comp_name=new_text.replace("(", "")                # remove extra paranthesis
        new_comp_name=new_comp_name.replace(")", "")           # remove extra paranthesis

        # print('new: ',new_comp_name)
        return new_comp_name


def building_blocks(compound, option='all'):
    if '(' in compound:
        compound=refine_chem_formula(compound)
    tmp_elem_lst=re.findall('[A-Z][^A-Z]*', compound)
    elements_lst=[]
    stoichiometry_lst=[]
    for i in tmp_elem_lst:
        # print("print 1:",i,len(i), re.findall('(\d+|[A-Za-z]+)', i) )
        elements_lst.append(re.findall('(\d+|[A-Za-z]+)', i)[0])
        if len(re.findall('(\d+|[A-Za-z]+)', i))==1:
            # print("Unit shoul be added")
            stoichiometry_lst.append(1)
        else:
            stoichiometry_lst.append( eval(re.findall(r"[-+]?(?:\d*\.*\d+)", i)[0]) )
    if option not in ['all', 'element', 'stoichiometry']: # if the opt argument is not one of the valid strings
        raise ValueError("Invalid keyword. Please inter one of the defined keywords for 'option' argument: `element` or `stoichiometry`.") # raise a ValueError with a message
    elif (option=='element'):
        return elements_lst
    elif (option=='stoichiometry'):
        return stoichiometry_lst
    else:
        return elements_lst, stoichiometry_lst



def building_blocks_df(dataframe_name,column_name):

    dataframe_name["Elements"]=dataframe_name[column_name].apply(building_blocks,option='element')
    dataframe_name["Number_of_Elements"]=dataframe_name["Elements"].apply(len)
    unique_elements=dataframe_name["Number_of_Elements"].unique()

    return dataframe_name

def get_feature_values(compound,feature_collection,feature_name):

    column_names=[]
    atoms = building_blocks(compound,'element')
    for idx in range(len(atoms)):
        column_names.append('{}_{}_{}'.format(feature_name,idx+1,atoms[idx]))
    mat_fea_vals=[]
    for atom in atoms:
        tmp_val = feature_collection.loc[feature_collection['chemical_symbol'] == atom,feature_name].values   ##########
        mat_fea_vals.append(tmp_val[0])

    return column_names, mat_fea_vals

def get_feature_values_df(dataframe_name,column_name,feature_collection,feature_name):
    
    #dataframe_name=dataframe_name_0.copy()  ##########
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
            dataframe_name.loc[dataframe_name.index[i],column_names[j]]=(dataframe_name['Feature'])[i][1][j]
    
    return dataframe_name.drop(["Feature","Elements","Number_of_Elements"],axis=1)

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


def fetch_features(compounds, collection, features='all', column_name=None):
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
        if (column_name==None):
            raise ValueError("The input is `pd.DataFrame` and `column_name` argument is not given. Please inter materials column name.")
        else :
            return get_features_df(compounds,column_name,collection,features)



