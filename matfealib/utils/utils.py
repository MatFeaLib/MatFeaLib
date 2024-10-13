import pandas as pd
import numpy as np
from ..atomicfeatures.base import building_blocks_df

def DatasetElements(dataframe_name, column_name):
    if isinstance(dataframe_name, pd.DataFrame):
        if isinstance(column_name, str):
            df = building_blocks_df(dataframe_name, column_name)
            tmp_lst=[]
            for i in range(len(df)):
                for j in df.Elements.iloc[i]:
                    tmp_lst.append(j)
            tmp_array = np.array(tmp_lst)
            chemical_symbol, counts = np.unique(tmp_array, return_counts=True)
            return pd.DataFrame({'chemical_symbol':chemical_symbol , 'count': counts})
        else:
            raise ValueError('The `column_name` is need.')
    else:
        raise ValueError('The Input should be in the form of pandas.DataFrame')




