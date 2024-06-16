
import pandas as pd
import plotly.graph_objects as go
from .base import periodic_table_custom, periodic_table_default

def periodic_table(
    heatmap: bool = False,
    data: pd.DataFrame = None,
    feature_name: str = None,
    cmap: str = 'Spectral_r',
    missing_color: str = "#ffffff",
    symbol_color: str = None,
    name_color: str = None,
    atomic_number_color: str = None,
    feature_color= None,
    colorbar: bool = True,
    transparent: bool = False,
    output_name: str = None,
    guidance_cell: bool = True,
    guidance_cell_symbol: str = None,
    border_color: str = None,
    cell_opacity: float = 0.8,
    color_guidance: bool = True,
    )-> go.Figure:

    if heatmap==True:
        if atomic_number_color==None:
            atomic_number_color="#333333"
        if symbol_color==None:
            symbol_color="#333333"
        if name_color==None:
            name_color="#333333"
        if feature_color==None:
            feature_color="#333333"
        return periodic_table_custom(
            data=data,
            feature_name=feature_name,
            cmap=cmap,
            missing_color=missing_color,
            symbol_color=symbol_color,
            name_color=name_color,
            atomic_number_color=atomic_number_color,
            feature_color=feature_color,
            colorbar=colorbar,
            transparent=transparent,
            output_name=output_name,
            guidance_cell=guidance_cell,
            guidance_cell_symbol=guidance_cell_symbol,
            border_color=border_color,
            cell_opacity=cell_opacity,
        )

    else:
        if atomic_number_color==None:
            atomic_number_color="#ffffff"
        if symbol_color==None:
            symbol_color="#ffffff"
        if name_color==None:
            name_color="#ffffff"
        if feature_color==None:
            feature_color="#ffffff"
        return periodic_table_default(
            data=data,
            feature_name=feature_name,
            symbol_color=symbol_color,
            name_color=name_color,
            atomic_number_color=atomic_number_color,
            feature_color=feature_color,
            transparent=transparent,
            output_name=output_name,
            guidance_cell=guidance_cell,
            guidance_cell_symbol=guidance_cell_symbol,
            border_color=border_color,
            cell_opacity=cell_opacity,
            color_guidance=color_guidance,
        )