'''
Folium_map_mod is used to create the folium map through the data_entry_map function 
'''
import folium
import os
import geopandas
import pandas as pd
import csv
import string
from folium.plugins import Draw
import load_utilities as lu

make_popupcontent = 'hello'

def change_prop(prop):
    
    '''
    Choosing the proprety to reference to create the pop_up 
    for the Folium map
    '''
    
    def make_popupcontent(feature):
        return "<em>{}</em>".format(feature["properties"][prop])
    return make_popupcontent

def data_entry_map(map_dir=None,style_function=None, labels_feature=None):
    '''
    Allows to create the Folium map importing a geojson and applying 
    a specif style function
    '''
    m = folium.Map(
        tiles='cartodbpositron'
    )
    
    if map_dir is not None:
        data = geopandas.GeoDataFrame.from_file(map_dir)
        
        if labels_feature is None: #handling the case when labels_feature is not provided
            labels_feature = lu.load_labels_feature(map_dir)
        
        make_popupcontent = change_prop(labels_feature) 
        #Using labels_feature to create the pop ups per the maps
        
        draw = Draw()

        draw.add_to(m)

        folium.GeoJson(data, popup_function=make_popupcontent, style_function=style_function).add_to(m)

        folium.LayerControl().add_to(m)
        
    return (m)
 

        
        
