
import pandas as pd
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
    df.columns=['collection','description']
    pd.set_option("display.max_colwidth", None)
#    df = df.style.set_properties(**{'text-align': 'left'})
#    df = df.set_table_styles([dict(selector = 'th', props=[('text-align', 'left')])])
    return df

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

