'''
load_utilies is used to load from search_dict.csv and config.csv 
the data need for SearchAlgo, pop_general, file_writer_mod
and Folium_map_mod
'''

import os
import json
import csv
import pandas as pd

def load_coor_data_from_file(filename):
    '''
    Loads the coor data by name given a tab separated csv
    '''
    
    data = pd.read_csv(filename, encoding='latin_1',sep=' ', index_col = 0)
    print(data)
    coor_dict = {}
    coor_dict = data['COOR'].to_dict()
    return coor_dict #load the dict of coordinates by name given a tab separated csv

def load_regions_list_from_file(filename): 
    '''
    Loads the list of regions by name given a tab separated csv
    '''
    
    regions_list = []
    with open(filename) as f:
        for line in f.readlines():
            zones_list = [x.strip() for x in line.split(' ')]
            regions_list.append(zones_list)

    return regions_list

def load_coor_data():
    '''
    Allows to choose among the csvs present in the directory 
    which is the one that contains the coordinate data for the regions 
    '''
    coor_csv_files = [csv_file for csv_file in os.listdir(os.getcwd()) if csv_file.endswith('.csv')]

    if len(coor_csv_files) == 1:
        coor_dict = load_coor_data_from_file(coor_csv_files[0])
    else:
        print('Missing or multiplecoor_data csv files')
        print(coor_csv_files[:])
        coor_csv_file = input('Which is the right file?')
        coor_dict = load_coor_data_from_file(coor_csv_file)

    return coor_dict

def load_regions_list():
    '''
    Allows to choose among the csvs present in the directory 
    which is the one that lists the search regions
    '''
    
    list_csv_files = [csv_file for csv_file in os.listdir(os.getcwd()) if csv_file.endswith('.csv')]

    if len(list_csv_files) == 1:
        regions_list = load_regions_list_from_file(list_csv_files[0])
    else:
        print('Missing or multiple list_REGIONS csv files')
        print(list_csv_files[:])
        list_csv_file = input('Which is the right file?')
        regions_list = load_regions_list_from_file(list_csv_file)

    return regions_list

def load_labels_feature(filename):#Discovers the feature for the names of the regions
    '''
    Asks the user to indicate the field that contains the names of the regions in the map
    '''
    
    with open(filename,"r") as f:
        data = json.load(f)

    features_list = list(data["features"][0]['properties'].keys())

    print('List of features from your map:\n')
    print(features_list[:])
    print('\n')

    labels_feature = input('Name exactly the feature that containes the labels(e.g. NAME): ')

    return labels_feature

def load_map_file(): #Discovers the GEOJSON map file
    '''
    Identifies and returns the geojson map choosen in the current directory 
    and asks the user to indicate the field that contains the names of the regions in the map
    '''
    
    map_geojson_files = [geojson_file for geojson_file in os.listdir(os.getcwd()) if geojson_file.endswith('.geojson')]

    if len(map_geojson_files) == 1:
        map = map_geojson_files[0]
        labels_feature = load_labels_feature(map)
    else:
        print('Missing or multiple MAP geojson files'+'\n')
        print(map_geojson_files[:])
        map = input('Which is the right file?')
        labels_feature = load_labels_feature(map)

    return map, labels_feature

def load_search_dict_from_path(data_path):
    '''
    Loads from search_dict.csv or asks the user the search groups and search terms
    consequently writing search_dict.csv
    '''
    
    search_groups_dict = {}

    if os.path.isfile('search_dict.csv') == False:
        adding_search_group = True
        while(adding_search_group):
            search_group = input('''Add new search_group, type stop otherwise - ''')
            if search_group.find('stop') == 0:
                adding_search_group = False
                print('Stop_Add_groups')

            search_terms_list = []
            adding_search_term = True

            while(adding_search_term and adding_search_group):

                search_term = input('''Add new search_term, type stop otherwise - ''')

                print(search_term)

                if search_term.find('stop') == 0:
                    adding_search_term = False
                    print('Stop_Add_terms')
                if adding_search_term:
                    print('Add_terms')
                    search_terms_list.append([search_term])

            if adding_search_group:
                search_groups_dict[search_group] = search_terms_list


        with open("search_dict.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile,quoting=csv.QUOTE_NONE, delimiter='|', quotechar='',escapechar='\\')

            writer.writerow(['SEARCH_GROUP,SEARCH_TERMS'])

            for key,entry in search_groups_dict.items():

                data = entry[0][0]
                for single_term in entry[1:]:
                    data = data + '$' + single_term[0]

                row = key + ',' + data

                writer.writerow([row])

    data = pd.read_csv('search_dict.csv', encoding='latin_1',sep=',', index_col = 0)
    print(data)
    search_groups_dict = data['SEARCH_TERMS'].to_dict()
    for search_group in search_groups_dict:
        print(search_group)
        search_terms = search_groups_dict[search_group].split('$')
        print(search_terms[:])
        search_groups_dict[search_group] = search_terms


    return search_groups_dict

def load_data_from_path_pop(data_path): 
        '''
    Loads search_groups_dict,search_groups_list,regions_list, map, labels_feature
    as needed in pop_general.py from a given directory
    '''
    os.chdir(data_path)

    search_groups_dict = load_search_dict_from_path(data_path)
    search_groups_list = list(search_groups_dict.keys())


    if os.path.isfile('config.csv'):
        data = pd.read_csv('config.csv', encoding='latin_1',sep=',', index_col = 0)
        data_files_dict = {}
        print(data)
        data_files_dict = data['FILE'].to_dict()

        regions_list_file = data_files_dict['regions_list'] #load the dict of coordinates by name given a tab separated csv
        regions_list = load_regions_list_from_file(regions_list_file)

        map = data_files_dict['map']
        labels_feature = data_files_dict['labels_feature']

    else:
        regions_list = load_regions_list()
        map, labels_feature = load_map_file()

    return search_groups_dict,search_groups_list,regions_list, map, labels_feature

def load_data_from_path_search(data_path):
    '''
    Loads search_groups_dict,search_groups_list, regions_list, coor_dict 
    as needed in SearchAlgo.py from a given directory
    '''
    
    os.chdir(data_path)

    search_groups_dict = load_search_dict_from_path(data_path)
    
    search_groups_list = list(search_groups_dict.keys())
    print(search_groups_list[:])

    if os.path.isfile('config.csv'):
        data = pd.read_csv('config.csv', encoding='latin_1',sep=',', index_col = 0)
        print(data)
        data_files_dict = {}
        data_files_dict = data['FILE'].to_dict()

        regions_list_file = data_files_dict['regions_list'] #load the dict of coordinates by name given a tab separated csv
        coor_dict_file = data_files_dict['coor_dict']

        coor_dict = load_coor_data_from_file(coor_dict_file)
        regions_list = load_regions_list_from_file(regions_list_file)
    else:
        regions_list = load_regions_list()
        coor_dict = load_coor_data()

    return search_groups_dict,search_groups_list, regions_list, coor_dict
