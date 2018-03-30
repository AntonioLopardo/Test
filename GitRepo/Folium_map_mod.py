import folium
import os
import geopandas
import pandas as pd
import csv
import string
import load_utilies as lu
from folium.plugins import Draw

data_dir = '/home/antoniolopardo/Desktop/myRNN/Test/GitRepo/example_camera_senato/Example/COLL_LAZIO_CAMERA_PLUR_2018.geojson'
make_popupcontent = 'hello'

def change_prop(prop):
    def make_popupcontent(feature):
        return "<em>{}</em>".format(feature["properties"][prop])
    return make_popupcontent

def data_entry_map(map_dir=None):
    m = folium.Map(
        tiles='cartodbpositron'
    )
    
    if map_dir is not None:
        data = geopandas.GeoDataFrame.from_file(map_dir)
        
        feature_name = lu.load_labels_feature(map_dir)
        
        make_popupcontent = change_prop(feature_name)
        
        draw = Draw()

        draw.add_to(m)

        folium.GeoJson(data, popup_function=make_popupcontent).add_to(m)

        folium.LayerControl().add_to(m)
        
    if os.path.isdir('draw_data'):
        print('Already in\n')
    else:
        os.mkdir('draw_data')

    return (m)
 

        
        