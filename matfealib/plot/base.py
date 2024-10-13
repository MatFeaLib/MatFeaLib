
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.cm import ScalarMappable
from plotly.graph_objs.layout import Shape, Annotation
import plotly.graph_objects as go
from pandas.api.types import is_float_dtype
import warnings

def matplotlib_to_plotly(cmap, pl_entries):
    h = 1.0/(pl_entries-1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])

    return pl_colorscale

colors_guidance = pd.DataFrame(
    dict(
        x = [3.5,3.5,3.5,3.5,3.5,6.0,6.0,6.0,6.0,6.0],
        y = [1.0,1.3,1.6,1.9,2.2,1.0,1.3,1.6,1.9,2.2],
        chemical_series = [
            'Alkali Metals', 'Alkaline Earth Metals', 
            'Transition Metals', 'Other Metals','Metalloids',
            'Non-metals', 'Halogens', 'Noble Gases', 'Lanthanides',
            'Actinides'
        ],
        color = [
            '#fdc235', '#f97927', '#2685c1', '#263d51', '#769191',
            '#ea2d59', '#4caed4', '#8b58ad', '#ff4b34', '#54bd4a'
        ],
    )
)

groups = pd.DataFrame(
    dict(
        x=[
            1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 
            12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0
        ],
        y=[
            1.0, 2.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 
            2.0, 2.0, 2.0, 2.0, 2.0, 1.0
        ],
        label=[
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
            '11', '12', '13', '14', '15', '16', '17', '18'
        ],
    )
)

elements_ref=pd.DataFrame({
    'symbol': {
        0: 'H', 1: 'He', 2: 'Li', 3: 'Be', 4: 'B', 5: 'C', 6: 'N', 
        7: 'O', 8: 'F', 9: 'Ne', 10: 'Na', 11: 'Mg', 12: 'Al', 
        13: 'Si', 14: 'P', 15: 'S', 16: 'Cl', 17: 'Ar', 18: 'K',
        19: 'Ca', 20: 'Sc', 21: 'Ti', 22: 'V', 23: 'Cr', 24: 'Mn', 
        25: 'Fe', 26: 'Co', 27: 'Ni', 28: 'Cu', 29: 'Zn', 30: 'Ga', 
        31: 'Ge', 32: 'As', 33: 'Se', 34: 'Br', 35: 'Kr', 36: 'Rb', 
        37: 'Sr', 38: 'Y', 39: 'Zr', 40: 'Nb', 41: 'Mo', 42: 'Tc', 
        43: 'Ru', 44: 'Rh', 45: 'Pd', 46: 'Ag', 47: 'Cd', 48: 'In', 
        49: 'Sn', 50: 'Sb', 51: 'Te', 52: 'I', 53: 'Xe', 54: 'Cs', 
        55: 'Ba', 56: 'La', 57: 'Ce', 58: 'Pr', 59: 'Nd', 60: 'Pm', 
        61: 'Sm', 62: 'Eu', 63: 'Gd', 64: 'Tb', 65: 'Dy', 66: 'Ho', 
        67: 'Er', 68: 'Tm', 69: 'Yb', 70: 'Lu', 71: 'Hf', 72: 'Ta', 
        73: 'W', 74: 'Re', 75: 'Os', 76: 'Ir', 77: 'Pt', 78: 'Au', 
        79: 'Hg', 80: 'Tl', 81: 'Pb', 82: 'Bi', 83: 'Po', 84: 'At', 
        85: 'Rn', 86: 'Fr', 87: 'Ra', 88: 'Ac', 89: 'Th', 90: 'Pa', 
        91: 'U', 92: 'Np', 93: 'Pu', 94: 'Am', 95: 'Cm', 96: 'Bk', 
        97: 'Cf', 98: 'Es', 99: 'Fm', 100: 'Md', 101: 'No', 102: 'Lr', 
        103: 'Rf', 104: 'Db', 105: 'Sg', 106: 'Bh', 107: 'Hs', 
        108: 'Mt', 109: 'Ds', 110: 'Rg', 111: 'Cn', 112: 'Nh', 
        113: 'Fl', 114: 'Mc', 115: 'Lv', 116: 'Ts', 117: 'Og', 
    },
    'name': {
        0: 'Hydrogen', 1: 'Helium', 2: 'Lithium', 3: 'Beryllium', 
        4: 'Boron', 5: 'Carbon', 6: 'Nitrogen', 7: 'Oxygen', 
        8: 'Fluorine', 9: 'Neon', 10: 'Sodium', 11: 'Magnesium', 
        12: 'Aluminum', 13: 'Silicon', 14: 'Phosphorus', 15: 'Sulfur', 
        16: 'Chlorine', 17: 'Argon', 18: 'Potassium', 19: 'Calcium', 
        20: 'Scandium', 21: 'Titanium', 22: 'Vanadium', 23: 'Chromium', 
        24: 'Manganese', 25: 'Iron', 26: 'Cobalt', 27: 'Nickel', 
        28: 'Copper', 29: 'Zinc', 30: 'Gallium', 31: 'Germanium', 
        32: 'Arsenic', 33: 'Selenium', 34: 'Bromine', 35: 'Krypton', 
        36: 'Rubidium', 37: 'Strontium', 38: 'Yttrium', 39: 'Zirconium',
        40: 'Niobium', 41: 'Molybdenum', 42: 'Technetium', 
        43: 'Ruthenium', 44: 'Rhodium', 45: 'Palladium', 46: 'Silver', 
        47: 'Cadmium', 48: 'Indium', 49: 'Tin', 50: 'Antimony', 
        51: 'Tellurium', 52: 'Iodine', 53: 'Xenon', 54: 'Cesium',
        55: 'Barium', 56: 'Lanthanum', 57: 'Cerium', 58: 'Praseodymium',
        59: 'Neodymium', 60: 'Promethium', 61: 'Samarium', 
        62: 'Europium', 63: 'Gadolinium', 64: 'Terbium', 
        65: 'Dysprosium', 66: 'Holmium', 67: 'Erbium', 68: 'Thulium', 
        69: 'Ytterbium', 70: 'Lutetium', 71: 'Hafnium', 72: 'Tantalum', 
        73: 'Tungsten', 74: 'Rhenium', 75: 'Osmium', 76: 'Iridium', 
        77: 'Platinum', 78: 'Gold', 79: 'Mercury', 80: 'Thallium', 
        81: 'Lead', 82: 'Bismuth', 83: 'Polonium', 84: 'Astatine',
        85: 'Radon', 86: 'Francium', 87: 'Radium', 88: 'Actinium', 
        89: 'Thorium', 90: 'Protactinium', 91: 'Uranium', 
        92: 'Neptunium', 93: 'Plutonium', 94: 'Americium', 95: 'Curium',
        96: 'Berkelium', 97: 'Californium', 98: 'Einsteinium', 
        99: 'Fermium', 100: 'Mendelevium', 101: 'Nobelium', 
        102: 'Lawrencium', 103: 'Rutherfordium', 104: 'Dubnium',
        105: 'Seaborgium', 106: 'Bohrium', 107: 'Hassium', 
        108: 'Meitnerium', 109: 'Darmstadtium', 110: 'Roentgenium', 
        111: 'Copernicium', 112: 'Nihonium', 113: 'Flerovium', 
        114: 'Moscovium', 115: 'Livermorium', 116: 'Tennessine', 
        117: 'Oganesson',
    },
    'atomic_number': { 
        0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 
        10: 11, 11: 12, 12: 13, 13: 14, 14: 15, 15: 16, 16: 17, 17: 18, 
        18: 19, 19: 20, 20: 21, 21: 22, 22: 23, 23: 24, 24: 25, 25: 26, 
        26: 27, 27: 28, 28: 29, 29: 30, 30: 31, 31: 32, 32: 33, 33: 34, 
        34: 35, 35: 36, 36: 37, 37: 38, 38: 39, 39: 40, 40: 41, 41: 42, 
        42: 43, 43: 44, 44: 45, 45: 46, 46: 47, 47: 48, 48: 49, 49: 50, 
        50: 51, 51: 52, 52: 53, 53: 54, 54: 55, 55: 56, 56: 57, 57: 58, 
        58: 59, 59: 60, 60: 61, 61: 62, 62: 63, 63: 64, 64: 65, 65: 66, 
        66: 67, 67: 68, 68: 69, 69: 70, 70: 71, 71: 72, 72: 73, 73: 74, 
        74: 75, 75: 76, 76: 77, 77: 78, 78: 79, 79: 80, 80: 81, 81: 82, 
        82: 83, 83: 84, 84: 85, 85: 86, 86: 87, 87: 88, 88: 89, 89: 90, 
        90: 91, 91: 92, 92: 93, 93: 94, 94: 95, 95: 96, 96: 97, 97: 98, 
        98: 99, 99: 100, 100: 101, 101: 102, 102: 103, 103: 104, 
        104: 105, 105: 106, 106: 107, 107: 108, 108: 109, 109: 110, 
        110: 111, 111: 112, 112: 113, 113: 114, 114: 115, 115: 116, 
        116: 117, 117: 118, 
    },
    'color': { 
        0: '#2ab0a1', 1: '#8b58ad', 2: '#fdc235', 3: '#f97927', 
        4: '#769191', 5: '#ea2d59', 6: '#ea2d59', 7: '#ea2d59', 
        8: '#4caed4', 9: '#8b58ad', 10: '#fdc235', 11: '#f97927', 
        12: '#263d51', 13: '#769191', 14: '#ea2d59', 15: '#ea2d59', 
        16: '#4caed4', 17: '#8b58ad', 18: '#fdc235', 19: '#f97927', 
        20: '#2685c1', 21: '#2685c1', 22: '#2685c1', 23: '#2685c1', 
        24: '#2685c1', 25: '#2685c1', 26: '#2685c1', 27: '#2685c1', 
        28: '#2685c1', 29: '#2685c1', 30: '#263d51', 31: '#769191', 
        32: '#769191', 33: '#ea2d59', 34: '#4caed4', 35: '#8b58ad', 
        36: '#fdc235', 37: '#f97927', 38: '#2685c1', 39: '#2685c1', 
        40: '#2685c1', 41: '#2685c1', 42: '#2685c1', 43: '#2685c1', 
        44: '#2685c1', 45: '#2685c1', 46: '#2685c1', 47: '#2685c1', 
        48: '#263d51', 49: '#263d51', 50: '#769191', 51: '#769191', 
        52: '#4caed4', 53: '#8b58ad', 54: '#fdc235', 55: '#f97927', 
        56: '#ff4b34', 57: '#ff4b34', 58: '#ff4b34', 59: '#ff4b34', 
        60: '#ff4b34', 61: '#ff4b34', 62: '#ff4b34', 63: '#ff4b34', 
        64: '#ff4b34', 65: '#ff4b34', 66: '#ff4b34', 67: '#ff4b34', 
        68: '#ff4b34', 69: '#ff4b34', 70: '#ff4b34', 71: '#2685c1', 
        72: '#2685c1', 73: '#2685c1', 74: '#2685c1', 75: '#2685c1', 
        76: '#2685c1', 77: '#2685c1', 78: '#2685c1', 79: '#2685c1', 
        80: '#263d51', 81: '#263d51', 82: '#263d51', 83: '#769191', 
        84: '#4caed4', 85: '#8b58ad', 86: '#fdc235', 87: '#f97927', 
        88: '#54bd4a', 89: '#54bd4a', 90: '#54bd4a', 91: '#54bd4a', 
        92: '#54bd4a', 93: '#54bd4a', 94: '#54bd4a', 95: '#54bd4a', 
        96: '#54bd4a', 97: '#54bd4a', 98: '#54bd4a', 99: '#54bd4a', 
        100: '#54bd4a', 101: '#54bd4a', 102: '#54bd4a', 103: '#2685c1', 
        104: '#2685c1', 105: '#2685c1', 106: '#2685c1', 107: '#2685c1', 
        108: '#2685c1', 109: '#2685c1', 110: '#2685c1', 111: '#2685c1', 
        112: '#263d51', 113: '#263d51', 114: '#263d51', 115: '#263d51', 
        116: '#4caed4', 117: '#8b58ad'
    },
    'x': {
        0: 1.0, 1: 18.0, 2: 1.0, 3: 2.0, 4: 13.0, 5: 14.0, 6: 15.0, 
        7: 16.0, 8: 17.0, 9: 18.0, 10: 1.0, 11: 2.0, 12: 13.0, 13: 14.0,
        14: 15.0, 15: 16.0, 16: 17.0, 17: 18.0, 18: 1.0, 19: 2.0, 
        20: 3.0, 21: 4.0, 22: 5.0, 23: 6.0, 24: 7.0, 25: 8.0, 26: 9.0, 
        27: 10.0, 28: 11.0, 29: 12.0, 30: 13.0, 31: 14.0, 32: 15.0, 
        33: 16.0, 34: 17.0, 35: 18.0, 36: 1.0, 37: 2.0, 38: 3.0, 
        39: 4.0, 40: 5.0, 41: 6.0, 42: 7.0, 43: 8.0, 44: 9.0, 45: 10.0, 
        46: 11.0, 47: 12.0, 48: 13.0, 49: 14.0, 50: 15.0, 51: 16.0, 
        52: 17.0, 53: 18.0, 54: 1.0, 55: 2.0, 56: 3.0, 57: 4.0, 58: 5.0,
        59: 6.0, 60: 7.0, 61: 8.0, 62: 9.0, 63: 10.0, 64: 11.0, 
        65: 12.0, 66: 13.0, 67: 14.0, 68: 15.0, 69: 16.0, 70: 17.0, 
        71: 4.0, 72: 5.0, 73: 6.0, 74: 7.0, 75: 8.0, 76: 9.0, 77: 10.0, 
        78: 11.0, 79: 12.0, 80: 13.0, 81: 14.0, 82: 15.0, 83: 16.0, 
        84: 17.0, 85: 18.0, 86: 1.0, 87: 2.0, 88: 3.0, 89: 4.0, 90: 5.0,
        91: 6.0, 92: 7.0, 93: 8.0, 94: 9.0, 95: 10.0, 96: 11.0, 
        97: 12.0, 98: 13.0, 99: 14.0, 100: 15.0, 101: 16.0, 102: 17.0, 
        103: 4.0, 104: 5.0, 105: 6.0, 106: 7.0, 107: 8.0, 108: 9.0, 
        109: 10.0, 110: 11.0, 111: 12.0, 112: 13.0, 113: 14.0, 
        114: 15.0, 115: 16.0, 116: 17.0, 117: 18.0
    },
    'y': {
        0: 1.0, 1: 1.0, 2: 2.0, 3: 2.0, 4: 2.0, 5: 2.0, 6: 2.0, 7: 2.0, 
        8: 2.0, 9: 2.0, 10: 3.0, 11: 3.0, 12: 3.0, 13: 3.0, 14: 3.0, 
        15: 3.0, 16: 3.0, 17: 3.0, 18: 4.0, 19: 4.0, 20: 4.0, 21: 4.0, 
        22: 4.0, 23: 4.0, 24: 4.0, 25: 4.0, 26: 4.0, 27: 4.0, 28: 4.0, 
        29: 4.0, 30: 4.0, 31: 4.0, 32: 4.0, 33: 4.0, 34: 4.0, 35: 4.0, 
        36: 5.0, 37: 5.0, 38: 5.0, 39: 5.0, 40: 5.0, 41: 5.0, 42: 5.0, 
        43: 5.0, 44: 5.0, 45: 5.0, 46: 5.0, 47: 5.0, 48: 5.0, 49: 5.0, 
        50: 5.0, 51: 5.0, 52: 5.0, 53: 5.0, 54: 6.0, 55: 6.0, 56: 8.5, 
        57: 8.5, 58: 8.5, 59: 8.5, 60: 8.5, 61: 8.5, 62: 8.5, 63: 8.5, 
        64: 8.5, 65: 8.5, 66: 8.5, 67: 8.5, 68: 8.5, 69: 8.5, 70: 8.5, 
        71: 6.0, 72: 6.0, 73: 6.0, 74: 6.0, 75: 6.0, 76: 6.0, 77: 6.0, 
        78: 6.0, 79: 6.0, 80: 6.0, 81: 6.0, 82: 6.0, 83: 6.0, 84: 6.0, 
        85: 6.0, 86: 7.0, 87: 7.0, 88: 9.5, 89: 9.5, 90: 9.5, 91: 9.5, 
        92: 9.5, 93: 9.5, 94: 9.5, 95: 9.5, 96: 9.5, 97: 9.5, 98: 9.5, 
        99: 9.5, 100: 9.5, 101: 9.5, 102: 9.5, 103: 7.0, 104: 7.0, 
        105: 7.0, 106: 7.0, 107: 7.0, 108: 7.0, 109: 7.0, 110: 7.0, 
        111: 7.0, 112: 7.0, 113: 7.0, 114: 7.0, 115: 7.0, 116: 7.0, 
        117: 7.0,
    }
})

def create_annotation(
    row: pd.Series,
    feature_name: str,
    font_size: int = 10,
    x_offset: float = 0.0,
    y_offset: float = 0.0,
    xanchor: str = 'auto',
    font_color: str = '#FFFFFF',
    font_family: str = "Roboto",
    font_opacity: int = 0.9,
) -> Annotation:
    """create text annotations.

    Create text annotations from a Pandas DataFrame row (pandas series).

    Parameters
    ----------
    row : pd.Series
        DataFrame's row
    feature_name: str
        Feature name
    font_size: int, default=10
        Font size
    x_offset: float, default=0.0
        x offset
    y_offset: float, default=0.0
        y offset
    xanchor: str, default='auto'
        xanchor
    font_color: str, default= '#FFFFFF'
        Font color
    font_family: str, default="Roboto"
        Font family
    font_opacity: int, defult=0.9,
        Font opacity

    Returns
    -------
    Annotation
        Text annotations for periodic table of elements.

    """
    return Annotation(
        x = row["x"] + x_offset,
        y = row["y"] + y_offset,
        xref = "x",
        yref = "y",
        text = row[feature_name],
        showarrow = False,
        font = dict(
            family=font_family, 
            size=font_size, 
            color=font_color
        ),
        align = "center",
        xanchor = xanchor,
        opacity = font_opacity,
    )

# Visualize Custemize Periodic Table
def periodic_table_custom(
    data: pd.DataFrame = None,
    feature_name: str = None,
    cmap: str = 'Spectral_r',
    missing_color: str = "#ffffff",
    symbol_color: str = "#333333",
    name_color: str = "#333333",
    atomic_number_color: str = "#333333",
    feature_color = "#333333",
    colorbar: bool = True,
    transparent: bool = False,
    output_name: str = None,
    guidance_cell: bool = True,
    guidance_cell_symbol: str = None,
    border_color: str = 'gray',
    cell_opacity: float = 0.8,
) -> go.Figure:
    """
    Function for ploting (custemize) periodic table heatmap of elements
    """
    # elements = pd.DataFrame(elements_dict)
    elements = elements_ref.copy()

    if data is not None:
        # data = data.dropna().copy()
        if feature_name is None:
            raise ValueError('Feature name is nessesary for '
                             'visualizing the periodic table. Please '
                             'set `feature_name` argument')
        else:
            data = data.dropna(subset = feature_name).copy()
            elements.loc[:, 'color'] = missing_color
            elements.loc[:, feature_name]  = np.NaN
            for i, smbl in enumerate(data.chemical_symbol):
                element_entry = elements.symbol[
                    elements.symbol.str.lower() == smbl.lower()
                ]
                if (element_entry.empty == True):
                    warnings.warn("Invalid chemical symbol: " + smbl, 
                                  ", please check your input.")

                elements.loc[elements.symbol.str.lower() == smbl.lower(), feature_name] = data.loc[data.chemical_symbol == smbl, feature_name].to_numpy()[0]

            # color mapping
            tmp_elements = elements.dropna(subset = feature_name)
            colormap = plt.get_cmap(cmap)
            cnorm = colors.Normalize(vmin = tmp_elements[feature_name].min(), vmax = tmp_elements[feature_name].max())
            scalarmap = ScalarMappable(norm = cnorm, cmap = colormap)
            rgba = scalarmap.to_rgba(tmp_elements[feature_name])
            tmp_elements.loc[:, 'color'] = [colors.rgb2hex(row) for row in rgba]

            for i in tmp_elements.symbol.tolist():
                elements.loc[elements.symbol.str.lower() == i.lower(), 'color'] = tmp_elements.loc[tmp_elements.symbol == i, 'color'].to_numpy()[0]
    else:
        raise ValueError("Data is nessesary for this fuction")

    fig = go.Figure()

    if border_color is None:
        elements['border_color'] = elements.color
    else:
        elements['border_color'] = border_color

    # insert cells
    cells = []
    for i in range(len(elements)):
        tmp_shap = Shape(
            type="rect",
            x0=elements.loc[i, "x"] - 0.45,
            y0=elements.loc[i, "y"] - 0.45,
            x1=elements.loc[i, "x"] + 0.45,
            y1=elements.loc[i, "y"] + 0.45,
            # line = dict(color=elements.loc[i,"color"]),
            line=dict(color=elements.loc[i, "border_color"]),
            fillcolor=elements.loc[i, "color"],
            opacity=cell_opacity)
        cells.append(tmp_shap)
    fig.layout["shapes"] += tuple(cells)

    # annotate groups labels
    fig.layout["annotations"] += tuple(
        groups.apply(
            create_annotation, 
            axis=1, 
            raw=False, 
            args=("label",), 
            font_size=12, 
            xanchor='auto', 
            y_offset=-0.6, 
            font_color='#444'
        )
    )

    # annotate symbols
    fig.layout["annotations"] += tuple(
        elements.apply(
            create_annotation, 
            axis=1, 
            raw=False, 
            args=("symbol",), 
            font_size=16, 
            font_family="Roboto Black", 
            font_color=symbol_color
        )
    )

    # annotate atomic_number
    fig.layout["annotations"] += tuple(
        elements.apply(
            create_annotation, 
            axis=1, 
            raw=False, 
            args=("atomic_number",), 
            y_offset=-0.3, 
            font_color=atomic_number_color
        )
    )

    # annotate name
    fig.layout["annotations"] += tuple(
        elements.apply(
            create_annotation, 
            axis=1, 
            raw=False, 
            args=("name",), 
            y_offset=0.2, 
            font_size=7, 
            font_color=name_color
        )
    )

    # annotate attribute
    if is_float_dtype(elements[feature_name]):
        decimals = 2
        elements["display_attribute"] = elements[feature_name].round(decimals=decimals)
    else:
        elements["display_attribute"] = elements[feature_name].dropna()

    # annotate attribute
    fig.layout["annotations"] += tuple(
        elements.dropna(subset=feature_name).apply(
            create_annotation, 
            axis=1, 
            raw=False, 
            args=("display_attribute",), 
            y_offset=0.35, 
            font_size=7, 
            font_color=feature_color,
        )
    )

    # Lanthanides cell (57-71)
    fig.layout["shapes"] += tuple([
        Shape(
            type="rect", 
            x0=3-0.45, 
            y0=6-0.45, 
            x1=3+0.45, 
            y1=6+0.45,
            line=dict(color='rgba(0, 0, 0, 0)'), 
            fillcolor='rgba(0, 0, 0, 0)',
        )
    ]
    )

    fig.layout["annotations"] += tuple([
        Annotation(
            x=3, 
            y=6, 
            xref="x", 
            yref="y", 
            text='57-71',
            font=dict(
                family="Roboto Black", size=12, color=symbol_color
            ),
            align="center", 
            showarrow=False, 
            opacity=0.9,
        ),
        Annotation(
            x=3, 
            y=6+0.2, 
            xref="x", 
            yref="y", 
            text='Lanthanides',
            font=dict(family="Roboto", size=7, color=symbol_color),
            align="center", 
            showarrow=False, 
            opacity=0.9,
        )
    ]
    )

    # Actinides cell (89-103)
    fig.layout["shapes"] += tuple([
        Shape(
            type="rect", 
            x0=3-0.45, 
            y0=7-0.45, 
            x1=3+0.45, 
            y1=7+0.45,
            line=dict(color='rgba(0, 0, 0, 0)'), 
            fillcolor='rgba(0, 0, 0, 0)',
        )
    ]
    )

    fig.layout["annotations"] += tuple([
        Annotation(
            x=3, 
            y=7, 
            xref="x", 
            yref="y", 
            text='89-103',
            font=dict(
                family="Roboto Black", size=12, color=symbol_color
            ),
            align="center", 
            showarrow=False, 
            opacity=0.9,
        ),
        Annotation(
            x=3, 
            y=7+0.2, 
            xref="x", 
            yref="y", 
            text='Actinides',
            font=dict(family="Roboto", size=7, color=symbol_color),
            align="center", 
            showarrow=False, 
            opacity=0.9,
        )
    ]
    )

    # atom guidance cell
    if (guidance_cell == True):
        if guidance_cell_symbol is None:
            # randomly selection an atom
            guidance_cell_symbol = tmp_elements.sample().symbol.to_numpy()[0]
        else:
            element_entry = tmp_elements.symbol[tmp_elements.symbol.str.lower() == guidance_cell_symbol.lower()]
            if (element_entry.empty == True):
                raise ValueError("Chemical symbol `{}` for `guidance_cell_symbol` argument is not in your DataFrame. Please select a chemical symbol from your input.".format(guidance_cell_symbol))
        fig.layout["shapes"] += tuple([
            Shape(
                type="rect",
                x0=9.0-0.45, 
                y0=1.5-0.45, 
                x1=9.0+0.45, 
                y1=1.5+0.45,
                line=dict(
                    color=elements.loc[elements.symbol == guidance_cell_symbol,"border_color"].to_numpy()[0]
                ),
                fillcolor=elements.loc[elements.symbol == guidance_cell_symbol,'color'].to_numpy()[0], 
                opacity=cell_opacity
            )
        ]
        )

        # atom annotations
        fig.layout["annotations"] += tuple([
            Annotation(
                x=9.0, 
                y=1.5-0.3, 
                xref="x", 
                yref="y", 
                text=str(elements.loc[elements.symbol == guidance_cell_symbol, 'atomic_number'].to_numpy()[0]),
                font=dict(
                    family="Roboto", size=10, color=atomic_number_color
                ),
                align="center", 
                showarrow=False,
                opacity=0.9,
            ),
            Annotation(
                x=9.0, 
                y=1.5, 
                xref="x", 
                yref="y", 
                text=guidance_cell_symbol,
                font=dict(
                    family="Roboto Black", size=16, color=symbol_color
                ),
                align="center", 
                showarrow=False,
                opacity=0.9,
            ),
            Annotation(
                x=9.0, 
                y=1.5+0.2, 
                xref="x", 
                yref="y", 
                text=elements.loc[elements.symbol == guidance_cell_symbol, 'name'].to_numpy()[0],
                font=dict(family="Roboto", size=7, color=name_color),
                align="center", 
                showarrow=False,
                opacity=0.9,
            )
        ]
        )

        # lines
        fig.layout["shapes"] += tuple([
            Shape(
                type="line",
                x0=9.0+0.25-1.2, 
                y0=1.5-0.3, 
                x1=9.0+1.0-1.2, 
                y1=1.5-0.3,
                line=dict(color="#000000", width=1),
                fillcolor="#2685c1", 
                opacity=0.8
            ),
            Shape(
                type="line",
                x0=9.0+0.25, 
                y0=1.5, 
                x1=9.0+1.0, 
                y1=1.5,
                line=dict(color="#000000", width=1),
                fillcolor="#2685c1", 
                opacity=0.8
            ),
            Shape(
                type="line",
                x0=9.0+0.40-1.35, 
                y0=1.5+0.2, 
                x1=9.0+1.0-1.35, 
                y1=1.5+0.2,
                line=dict(color="#000000", width=1),
                fillcolor="#2685c1", 
                opacity=0.8
            )
        ]
        )

        # guidance cell texts
        fig.layout["annotations"] += tuple([
            Annotation(
                x=10.05-4+0.4, 
                y=1.5-0.3, 
                xref="x", 
                yref="y", 
                text='Atomic Number',
                font=dict(family="Roboto", size=12, color="#333333"),
                align="center", 
                xanchor='left', 
                showarrow=False,
                opacity=0.9,
            ),
            Annotation(
                x=10.05, 
                y=1.5, 
                xref="x", 
                yref="y", 
                text='Symbol',
                font=dict(family="Roboto", size=12, color="#333333"),
                align="center", 
                xanchor='left', 
                showarrow=False, 
                opacity=0.9,
            ),
            Annotation(
                x=10.05-3+0.3, 
                y=1.7, 
                xref="x", 
                yref="y", 
                text='Name',
                font=dict(family="Roboto", size=12, color="#333333"),
                align="center", 
                xanchor='left', 
                showarrow=False,
                opacity=0.9,
            )
        ]
        )

        # line for guidance
        fig.layout["shapes"] += tuple([
            Shape(
                type="line",
                x0=9.0+0.25, 
                y0=1.5+0.35, 
                x1=9.0+1.0, 
                y1=1.5+0.35,
                line=dict(color="#000000", width=1),
                fillcolor="#2685c1", 
                opacity=0.8
            ),
        ]
        )

        # annonate for guidance
        fig.layout["annotations"] += tuple([
            Annotation(
                x=10.05, 
                y=1.5+0.35, 
                xref="x", 
                yref="y", 
                text=feature_name.capitalize(),
                font=dict(family="Roboto", size=12, color="#333333"),
                align="center", 
                xanchor='left', 
                showarrow=False,
                opacity=0.9,
            ),
            Annotation(
                x=9.0, y=1.5+0.35, xref="x", yref="y", 
                text=elements.loc[elements.symbol == guidance_cell_symbol, "display_attribute"].to_numpy()[0],
                font=dict(family="Roboto", size=7, color=feature_color),
                align="center", 
                xanchor='auto', 
                showarrow=False,
                opacity=0.9,
            )
        ]
        )

    tickvals = np.array(range(1, 19))
    xrange = [0.5, 18.5]
    yrange = [10.0, 0.5]

    # title: str = "Periodic Table"
    title: str = None
    height: int = 800
    width: int = 1200
    # height: int = 1080
    # width: int = 1920
    fig.update_layout(
        template="plotly_white",
        height=height,
        width=width,
        title=title,
        xaxis={
            "range": xrange,
            "showgrid": False,
            "fixedrange": True,
            "side": "top",
            # "tickvals": tickvals,
            # 'showticklabels': False
            # 'tickmode' : 'array',
            'tickvals' : [ 1, 18],
            'ticktext' : ['1','18'],
            'tickfont_color': '#444',
            'tickfont_family': 'Roboto'
        },
        yaxis={
            "range": yrange,
            "showgrid": False,
            "fixedrange": True,
            "tickvals": tuple(range(1, 8)),
            # "title": "Period",
            'tickfont_color': '#444',
            'tickfont_family': 'Roboto'
        }
    )

    # colorbar
    if (colorbar == True):
        colorbar_trace = go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(
                # colorscale='plasma', 
                colorscale = matplotlib_to_plotly(colormap, 255), 
                showscale=True,
                cmin=data[feature_name].min(),
                cmax=data[feature_name].max(),
                # colorbar=dict(thickness=20, showticklabels=True, tickcolor='gray', y=0.6, len=0.7),# tickvals=[-5, 5], ticktext=['Low', 'High']), 
                colorbar=dict(
                    thickness=15, 
                    showticklabels=True, 
                    tickcolor='gray', 
                    outlinecolor='rgba(0, 0, 0, 0)'
                ),
                opacity=0.8
            ),
            # hoverinfo=None,
            hoverinfo='skip'
        )
        fig.add_trace(colorbar_trace)
        fig.update_layout(modebar=dict(remove=['lasso', 'select']))

    if (transparent == True):
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        }
        )

    if output_name is not None:
        fig.write_image(output_name, scale=4)

    # fig.show()
    return fig


# Visualize Periodic Table whit predefined chemical series colors
def periodic_table_default(
    data: pd.DataFrame = None,
    feature_name: str = None,
    symbol_color: str = "#ffffff",
    name_color: str = "#ffffff",
    atomic_number_color: str = "#ffffff",
    feature_color= "#ffffff",
    color_guidance: bool = True,
    transparent: bool = False,
    output_name: str = None,
    guidance_cell: bool = True,
    guidance_cell_symbol: str = None,
    border_color: str = None,
    cell_opacity: float = 0.9,
    ) -> go.Figure:
    """
    Function for ploting periodic table of elements.
    """
    elements = elements_ref.copy()
    if (data is None and feature_name is not None):
        raise ValueError('Data is not inserted.')
    if data is not None:
        if feature_name is None:
            raise ValueError('Feature name is nessesary for visualizing the periodic table. Please set `feature_name` argument')
        else:
            data = data.dropna(subset=feature_name).copy()
            elements.loc[:, feature_name] = np.NaN
            for i, smbl in enumerate(data.chemical_symbol):
                element_entry = elements.symbol[elements.symbol.str.lower() == smbl.lower()]
                if (element_entry.empty == True):
                    warnings.warn("Invalid chemical symbol: " + smbl, ", please check your input.")
                elements.loc[elements.symbol.str.lower() == smbl.lower(), feature_name] = data.loc[data.chemical_symbol == smbl, feature_name].to_numpy()[0]
            tmp_elements = elements.dropna(subset=feature_name)

    else:
        tmp_elements = elements.dropna(subset=feature_name)

    fig = go.Figure()

    if border_color is None:
        elements['border_color'] = elements.color
    else:
        elements['border_color'] = border_color

    # insert cells
    cells = []
    for i in range(len(elements)):
        tmp_shap = Shape(
            type="rect",
            x0=elements.loc[i, "x"] - 0.45,
            y0=elements.loc[i, "y"] - 0.45,
            x1=elements.loc[i, "x"] + 0.45,
            y1=elements.loc[i, "y"] + 0.45,
            # line=dict(color=elements.loc[i,"color"]),
            line=dict(color=elements.loc[i, "border_color"]),
            fillcolor=elements.loc[i, "color"],
            opacity=cell_opacity
        )
        cells.append(tmp_shap)
    fig.layout["shapes"] += tuple(cells)

    # annotate groups labels
    fig.layout["annotations"] += tuple(
        groups.apply(
            create_annotation, 
            axis=1, 
            raw=False, 
            args=("label",), 
            font_size=12, 
            xanchor='auto', 
            y_offset=-0.6, 
            font_color='#444'
        )
    )

    # annotate symbols
    fig.layout["annotations"] += tuple(
        elements.apply(
            create_annotation, 
            axis=1, 
            raw=False, 
            args=("symbol",), 
            font_size=16, 
            font_family="Roboto Black", 
            font_color=symbol_color
        )
    )

    # annotate atomic_number
    fig.layout["annotations"] += tuple(
        elements.apply(
            create_annotation, 
            axis=1, 
            raw=False, 
            args=("atomic_number",), 
            y_offset=-0.3, 
            font_color=atomic_number_color
        )
    )

    # annotate name
    fig.layout["annotations"] += tuple(
        elements.apply(
            create_annotation, 
            axis=1, 
            raw=False, 
            args=("name",), 
            y_offset=0.2, 
            font_size=7, 
            font_color=name_color
        )
    )

    # annotate attribute
    if feature_name is not None:
        if is_float_dtype(elements[feature_name]):
            decimals = 2
            elements["display_attribute"] = elements[feature_name].round(decimals=decimals)
        else:
            elements["display_attribute"] = elements[feature_name].dropna()
        # annotate attribute
        fig.layout["annotations"] += tuple(
            elements.dropna(subset=feature_name).apply(
                create_annotation, 
                axis=1, 
                raw=False, 
                args=("display_attribute",), 
                y_offset=0.35, 
                font_size=7, 
                font_color=feature_color,
            )
        )

    # Lanthanides cell (57-71)
    fig.layout["shapes"] += tuple([
        Shape(
            type="rect", 
            x0=3-0.45, y0=6-0.45, 
            x1=3+0.45, y1=6+0.45,
            line=dict(color='#ff4b34'), 
            fillcolor='#ff4b34', 
            opacity=cell_opacity
        )
    ]
    )

    fig.layout["annotations"] += tuple([
        Annotation(
            x=3, 
            y=6, 
            xref="x", 
            yref="y", 
            text='57-71',
            font=dict(
                family="Roboto Black", size=12, color=symbol_color
            ),
            align="center", 
            showarrow=False, 
            opacity=0.9
        ),
        Annotation(
            x=3, y=6+0.2, xref="x", yref="y", 
            text='Lanthanides',
            font=dict(family="Roboto", size=7, color=symbol_color),
            align="center", 
            showarrow=False, 
            opacity=0.9
        )
    ]
    )

    # Actinides cell (89-103)
    fig.layout["shapes"] += tuple([
        Shape(
            type="rect", 
            x0=3-0.45, 
            y0=7-0.45, 
            x1=3+0.45, 
            y1=7+0.45,
            line=dict(color='#54bd4a'), 
            fillcolor='#54bd4a', 
            opacity=cell_opacity
        )
    ]
    )

    fig.layout["annotations"] += tuple([
        Annotation(
            x=3, 
            y=7, 
            xref="x", 
            yref="y", 
            text='89-103',
            font=dict(
                family="Roboto Black", size=12, color=symbol_color
            ),
            align="center", 
            showarrow=False, 
            opacity=0.9,
        ),
        Annotation(
            x=3, 
            y=7+0.2, 
            xref="x", 
            yref="y", 
            text='Actinides',
            font=dict(family="Roboto", size=7, color=symbol_color),
            align="center", 
            showarrow=False, 
            opacity=0.9,
        )
    ]
    )

    # atom guidance cell
    if (guidance_cell == True):
        if guidance_cell_symbol is None:
            # randomly selection an atom
            guidance_cell_symbol = tmp_elements.sample().symbol.to_numpy()[0]
        else:
            element_entry = tmp_elements.symbol[tmp_elements.symbol.str.lower() == guidance_cell_symbol.lower()]
            if (element_entry.empty == True):
                raise ValueError("Chemical symbol `{}` for `guidance_cell_symbol` argument is not in your DataFrame. Please select a chemical symbol from your input.".format(guidance_cell_symbol))
            # else:
        fig.layout["shapes"] += tuple([
            Shape(
                type="rect",
                x0=9.0-0.45, 
                y0=1.5-0.45, 
                x1=9.0+0.45, 
                y1=1.5+0.45,
                # line=dict(color=elements.loc[elements.symbol==atom,'color'].to_numpy()[0]),
                line=dict(color=elements.loc[elements.symbol == guidance_cell_symbol, "border_color"].to_numpy()[0]),
                fillcolor=elements.loc[elements.symbol == guidance_cell_symbol,'color'].to_numpy()[0], 
                opacity=cell_opacity
            )
        ]
        )

        # atom annotations
        fig.layout["annotations"] += tuple([
            Annotation(
                x=9.0, 
                y=1.5-0.3, 
                xref="x", 
                yref="y", 
                text=str(elements.loc[elements.symbol == guidance_cell_symbol,'atomic_number'].to_numpy()[0]),
                font=dict(
                    family="Roboto", size=10, color=atomic_number_color
                ),
                align="center", 
                showarrow=False,
                opacity=0.9,
            ),
            Annotation(
                x=9.0, 
                y=1.5, 
                xref="x", 
                yref="y", 
                text=guidance_cell_symbol,
                font=dict(
                    family="Roboto Black", size=16, color=symbol_color
                ),
                align="center", 
                showarrow=False,
                opacity=0.9,
            ),
            Annotation(
                x=9.0, 
                y=1.5+0.2, 
                xref="x", 
                yref="y", 
                text=elements.loc[elements.symbol == guidance_cell_symbol,'name'].to_numpy()[0],
                font=dict(family="Roboto", size=7, color=name_color),
                align="center", 
                showarrow=False,
                opacity=0.9,
            )
        ]
        )

        # lines
        fig.layout["shapes"] += tuple([
            Shape(
                type="line",
                x0=9.0+0.25, 
                y0=1.5-0.3, 
                x1=9.0+1.0, 
                y1=1.5-0.3,
                line=dict(color="#000000", width=1),
                fillcolor="#2685c1", 
                opacity=0.8
            ),
            Shape(
                type="line",
                x0=9.0+0.25, 
                y0=1.5, 
                x1=9.0+1.0, 
                y1=1.5,
                line=dict(color="#000000", width=1),
                fillcolor="#2685c1", 
                opacity=0.8
            ),
            Shape(
                type="line",
                x0=9.0+0.40, 
                y0=1.5+0.2, 
                x1=9.0+1.0, 
                y1=1.5+0.2,
                line=dict(color="#000000", width=1),
                fillcolor="#2685c1", 
                opacity=0.8
            )
        ]
        )

        # guidance cell texts
        fig.layout["annotations"] += tuple([
            Annotation(
                x=10.05, 
                y=1.5-0.3, 
                xref="x", 
                yref="y", 
                text='Atomic Number',
                font=dict(family="Roboto", size=10, color="#333333"),
                align="center", 
                xanchor='left', 
                showarrow=False,
                opacity=0.9,
            ),
            Annotation(
                x=10.05, 
                y=1.5, 
                xref="x", 
                yref="y", 
                text='Symbol',
                font=dict(family="Roboto", size=10, color="#333333"),
                align="center", 
                xanchor='left', 
                showarrow=False, 
                opacity=0.9,
            ),
            Annotation(
                x=10.05, 
                y=1.7, 
                xref="x", 
                yref="y", 
                text='Name',
                font=dict(family="Roboto", size=10, color="#333333"),
                align="center", 
                xanchor='left', 
                showarrow=False,
                opacity=0.9,
            )
        ]
        )

        if feature_name is not None:
            # line for guidance
            fig.layout["shapes"] += tuple([
                Shape(
                    type="line",
                    x0=9.0+0.25, 
                    y0=1.5+0.35, 
                    x1=9.0+1.0, 
                    y1=1.5+0.35,
                    line=dict(color="#000000", width=1),
                    fillcolor="#2685c1", 
                    opacity=0.8
                ),
            ]
            )

            # annonate for guidance
            fig.layout["annotations"] += tuple([
                Annotation(
                    x=10.05, 
                    y=1.5+0.35, 
                    xref="x", 
                    yref="y", 
                    text=feature_name.capitalize(),
                    font=dict(
                        family="Roboto", size=10, color="#333333"
                    ),
                    align="center", 
                    xanchor='left', 
                    showarrow=False,
                    opacity=0.9,
                ),
                Annotation(
                    x=9.0, 
                    y=1.5+0.35, 
                    xref="x", 
                    yref="y", 
                    text=elements.loc[elements.symbol == guidance_cell_symbol, "display_attribute"].to_numpy()[0],
                    font=dict(
                        family="Roboto", size=7, color=feature_color
                    ),
                    align="center", 
                    xanchor='auto', 
                    showarrow=False,
                    opacity=0.9,
                )
            ]
            )

    tickvals = np.array(range(1, 19))
    xrange = [0.5, 18.5]
    yrange = [10.0, 0.5]

    # title: str = "Periodic Table"
    title: str = None
    height: int = 800
    width: int = 1200
    # height: int = 1080
    # width: int = 1920
    fig.update_layout(
        template="plotly_white",
        height=height,
        width=width,
        title=title,
        xaxis={
            "range": xrange,
            "showgrid": False,
            "fixedrange": True,
            "side": "top",
            # "tickvals": tickvals,
            # 'showticklabels': False
            # 'tickmode' : 'array',
            'tickvals' : [ 1, 18],
            'ticktext' : ['1','18'],
            'tickfont_color': '#444',
            'tickfont_family': 'Roboto'
        },
        yaxis={
            "range": yrange,
            "showgrid": False,
            "fixedrange": True,
            "tickvals": tuple(range(1, 8)),
            # "title": "Period",
            'tickfont_color': '#444',
            'tickfont_family': 'Roboto'
        }
    )

    # color guidence
    if (color_guidance == True):
        cells = []
        for i in range(len(colors_guidance)):
            tmp_shap=Shape(
                type="rect",
                x0=colors_guidance.loc[i, "x"] - 0.1,
                y0=colors_guidance.loc[i, "y"] - 0.1,
                x1=colors_guidance.loc[i, "x"] + 0.1,
                y1=colors_guidance.loc[i, "y"] + 0.1,
                line=dict(color=colors_guidance.loc[i, "color"]),
                fillcolor=colors_guidance.loc[i, "color"],
                opacity=cell_opacity,
            )
            cells.append(tmp_shap)
        fig.layout["shapes"] += tuple(cells)
    
        fig.layout["annotations"] += tuple(
            colors_guidance.apply(
                create_annotation, 
                axis=1, 
                raw=False, 
                args=("chemical_series",), 
                font_size=9, 
                xanchor='left', 
                x_offset=0.2, 
                font_color='#333333'
            )
        )

    if (transparent == True):
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        }
        )

    if output_name is not None:
        fig.write_image(output_name, scale=5)

    # fig.show()
    return fig

