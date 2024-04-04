
import pandas as pd
import re


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


# def building_blocks(compound, option='all'):
#     if '(' in compound:
#         compound=refine_chem_formula(compound)
#     tmp_elem_lst=re.findall('[A-Z][^A-Z]*', compound)
#     elements_lst=[]
#     stoichiometry_lst=[]
#     for i in tmp_elem_lst:
#         # print("print 1:",i,len(i), re.findall('(\d+|[A-Za-z]+)', i) )
#         elements_lst.append(re.findall('(\d+|[A-Za-z]+)', i)[0])
#         if len(re.findall('(\d+|[A-Za-z]+)', i))==1:
#             # print("Unit shoul be added")
#             stoichiometry_lst.append(1)
#         else:
#             stoichiometry_lst.append( eval(re.findall(r"[-+]?(?:\d*\.*\d+)", i)[0]) )
#     if option not in ['all', 'element', 'stoichiometry']: # if the opt argument is not one of the valid strings
#         raise ValueError("Invalid keyword. Please inter one of the defined keywords for 'option' argument: `element` or `stoichiometry`.") # raise a ValueError with a message
#     elif (option=='element'):
#         return elements_lst
#     elif (option=='stoichiometry'):
#         return stoichiometry_lst
#     else:
#         return elements_lst, stoichiometry_lst


# Feb. 2, 2024 (13 Bahman 1402)
elements_iupac = ['Ac', 'Ag', 'Al', 'Am', 'Ar', 'As', 'At', 'Au', 'B', 'Ba', 'Be', 'Bh', 'Bi', 'Bk', 'Br',
  'C', 'Ca', 'Cd', 'Ce', 'Cf', 'Cl', 'Cm', 'Cn', 'Co', 'Cr', 'Cs', 'Cu', 'Db', 'Ds', 'Dy', 
  'Er', 'Es', 'Eu', 'F', 'Fe', 'Fl', 'Fm', 'Fr', 'Ga', 'Gd', 'Ge', 'H', 'He', 'Hf', 'Hg',
  'Ho', 'Hs', 'I', 'In', 'Ir', 'K', 'Kr', 'La', 'Li', 'Lr', 'Lu', 'Lv', 'Mc', 'Md', 'Mg',
  'Mn', 'Mo', 'Mt', 'N', 'Na', 'Nb', 'Nd', 'Ne', 'Nh', 'Ni', 'No', 'Np', 'O', 'Og', 'Os',
  'P', 'Pa', 'Pb', 'Pd', 'Pm', 'Po', 'Pr', 'Pt', 'Pu', 'Ra', 'Rb', 'Re', 'Rf', 'Rg', 'Rh',
  'Rn', 'Ru', 'S', 'Sb', 'Sc', 'Se', 'Sg', 'Si', 'Sm', 'Sn', 'Sr', 'Ta', 'Tb', 'Tc', 'Te', 
  'Th', 'Ti', 'Tl', 'Tm', 'Ts', 'U', 'V', 'W', 'Xe', 'Y', 'Yb', 'Zn', 'Zr']

def building_blocks(compound, option='all'):
    if '(' in compound:
        compound=refine_chem_formula(compound)
    tmp_elem_lst=re.findall('[A-Z][^A-Z]*', compound)
    elements_lst=[]
    stoichiometry_lst=[]

    for i in tmp_elem_lst:
        # print("print 1:",i,len(i), re.findall('(\d+|[A-Za-z]+)', i) )
        element_symbol = re.findall('(\d+|[A-Za-z]+)', i)[0]
        if element_symbol in elements_iupac:
            # print(element_symbol)
            elements_lst.append(element_symbol)
            if len(re.findall('(\d+|[A-Za-z]+)', i))==1:
                # print("Unit shoul be added")
                stoichiometry_lst.append(1)
            else:
                stoichiometry_lst.append( eval(re.findall(r"[-+]?(?:\d*\.*\d+)", i)[0]) )
        else:
            # print("2",element_symbol)
            raise ValueError("Invalid element name `{}`. The `{}` sample contain(s) element(s) that are not in standard list of IUPAC elements.".format(element_symbol,compound))

    if option not in ['all', 'element', 'stoichiometry']: # if the opt argument is not one of the valid strings
        raise ValueError("Invalid keyword. Please inter one of the defined keywords for 'option' argument: `element` or `stoichiometry`.") # raise a ValueError with a message
    elif (option=='element'):
        return elements_lst
    elif (option=='stoichiometry'):
        return stoichiometry_lst
    else:
        return elements_lst, stoichiometry_lst


# def building_blocks_df(dataframe_name,column_name):

#     dataframe_name["Elements"]=dataframe_name[column_name].apply(building_blocks,option='element')
#     dataframe_name["Number_of_Elements"]=dataframe_name["Elements"].apply(len)
#     unique_elements=dataframe_name["Number_of_Elements"].unique()

#     return dataframe_name

# 27 Azar 1402 - 23:13
# def building_blocks_df(dataframe_name,column_name,option='element'):

#     if (option=='element'):
#         dataframe_name["Elements"]=dataframe_name[column_name].apply(building_blocks,option='element')
#         dataframe_name["Number_of_Elements"]=dataframe_name["Elements"].apply(len)
#     elif (option=='stoichiometry'):
#         dataframe_name["Stoichiometry"]=dataframe_name[column_name].apply(building_blocks,option='stoichiometry')
#     else:
#         dataframe_name["all"]=dataframe_name[column_name].apply(building_blocks,option=option)
#     return dataframe_name

# 24 Bahman 1402 - 22:17
def building_blocks_df(dataframe_name,column_name,option='element'):

    df=dataframe_name.copy(deep=True)
    if (option=='element'):
        df["Elements"]=df[column_name].apply(building_blocks,option='element')
        df["Number_of_Elements"]=df["Elements"].apply(len)
    elif (option=='stoichiometry'):
        df["Stoichiometry"]=df[column_name].apply(building_blocks,option='stoichiometry')
    else:
        df["all"]=df[column_name].apply(building_blocks,option=option)
    return df






