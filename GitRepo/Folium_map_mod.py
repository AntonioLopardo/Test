import folium
import os
import geopandas
import pandas as pd
import csv
import string
from folium.plugins import Draw
import load_utilies as lu

make_popupcontent = 'hello'

def change_prop(prop):
    def make_popupcontent(feature):
        return "<em>{}</em>".format(feature["properties"][prop])
    return make_popupcontent

def data_entry_map(map_dir=None,style_function=None, labels_feature=None):
    m = folium.Map(
        tiles='cartodbpositron'
    )
    
    if map_dir is not None:
        data = geopandas.GeoDataFrame.from_file(map_dir)
        
        if labels_feature is None:
            labels_feature = lu.load_labels_feature(map_dir)
        
        make_popupcontent = change_prop(labels_feature)
        
        draw = Draw()

        draw.add_to(m)

        folium.GeoJson(data, popup_function=make_popupcontent, style_function=style_function).add_to(m)

        folium.LayerControl().add_to(m)
        
    if os.path.isdir('draw_data'):
        print('Already in\n')
    else:
        os.mkdir('draw_data')

    return (m)
 

        
        
