import TweetSearch as ts
import os
import time
import pandas as pd
import datetime as dt

def load_coor_data_from_file(filename):
    data = pd.read_csv(filename, encoding='latin_1',sep=' ', index_col = 0)
    coor_dict = {}
    coor_dict = data['COOR'].to_dict()
    return coor_dict #load the dict of coordinates by name given a tab separated csv

def load_regions_list_from_file(filename): #load the list of regions by name given a tab separated csv
    regions_list = []
    with open(filename) as f:
        for line in f.readlines():
            zones_list = [x.strip() for x in line.split(' ')]
            regions_list.append(zones_list)

    return regions_list

def load_coor_data():#Discovers the CSV COOR DATA loading the dict of coordinates
    coor_csv_files = [csv_file for csv_file in os.listdir(os.getcwd()) if csv_file.endswith('.csv')]

    if len(coor_csv_files) == 1:
        coor_dict = load_coor_data_from_file(coor_csv_files[0])
    else:
        print('Missing or multiplecoor_data csv files')
        print(coor_csv_files[:])
        coor_csv_file = input('Which is the right file?')
        coor_dict = load_coor_data_from_file(coor_csv_file)

    return coor_dict

def load_regions_list():#Discovers the CSV REGIONS loading the list of regions
    list_csv_files = [csv_file for csv_file in os.listdir(os.getcwd()) if csv_file.endswith('.csv')]

    if len(list_csv_files) == 1:
        regions_list = load_regions_list_from_file(list_csv_files[0])
    else:
        print('Missing or multiple list_REGIONS csv files')
        print(list_csv_files[:])
        list_csv_file = input('Which is the right file?')
        regions_list = load_regions_list_from_file(list_csv_file)

    return regions_list

def load_data_from_path_search(data_path): #Changes directory and loads the search_groups_list,regions_list, map from the directory given by looking for matching file extesions
    os.chdir(data_path)

    search_groups_list = [search_group_folder for search_group_folder in os.listdir(os.getcwd()) if (os.path.isdir(search_group_folder) and search_group_folder != '__pycache__' and search_group_folder != '.ipynb_checkpoints'  )]
    
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

    return search_groups_list, regions_list, coor_dict



def main():
    
    data_path = input('Where do you keep the data:')

    search_groups_list, regions_list, coor_dict = load_data_from_path_search(data_path)

    data_dir = os.getcwd()
    
    for search_group in search_groups_list:
        dir_pre_search_group = os.getcwd()
        search_group_path = dir_pre_search_group + '/' + search_group
        if os.path.isdir(search_group):
            print('Already in\n')
        else:
            os.mkdir(search_group_path)
        os.chdir(search_group_path)
        for region in regions_list:
            for zone in region:
                curr_dir = os.getcwd()
                zone_path = search_group_path + '/' + zone
                if os.path.isdir(zone):
                    print('Already in\n')
                else:
                    os.mkdir(zone_path)
        
    

    Destra = ['Lega OR ForzaItalia OR Salvini OR matteosalvini OR salvini OR Meloni OR FI OR Berlusconi OR berlusconi']
    Sinistra = ['PD OR Renzi OR renzi OR Gentiloni OR gentiloni OR Bonino OR +europa' ]
    M5S = ['M5S OR Di Maio OR DiMaio OR Grillo OR DiBattista OR Di Battista OR grillo']

    search_groups_dict = {}
    search_groups_dict['Destra'] = Destra
    search_groups_dict['Sinistra'] = Sinistra
    search_groups_dict['M5S'] = M5S

    print(regions_list[:])

    min_days_old, max_days_old = 0,7 #setting limits for age of the tweets
    max_search_counter = len(search_groups_list)
    search_counter = 0 #running counter for the search_groups

    for search_group in search_groups_list: #looping over the search groups
        search_counter += 1
        dir_pre_group = os.getcwd()
        dir_string = dir_pre_group + '/' + search_group
        os.chdir(dir_string)#moving in the search_group's dir
        max_reg_counter = len(regions_list)
        reg_counter = 0 #running counter for the regions

        for region in regions_list: #looping over the regions
            reg_counter += 1
            max_zone_counter = len(region)
            zone_counter = 0 #running counter for the zones

            for zone in region:
                zone_counter += 1
                dir_pre_zone = os.getcwd()
                dir_string = dir_pre_zone + '/' + zone
                os.chdir(dir_string) #moving in the zone's dir
                search_phrases = search_groups_dict[search_group]
                zone_coordinates = coor_dict[zone]
                time.sleep(1)
                done = 0
                while done == 0: #stay in until the search for the current phrase in the current zone is done
                    try:
                        ts.dist_search(zone_coordinates,
                                   search_phrases,
                                   min_days_old,
                                   max_days_old)
                        done = 1
                        print('\n'+str(search_counter)+'/'+str(max_search_counter)+ '-' +str(reg_counter)+'/'+str(max_reg_counter) + '-' + str(zone_counter)+'/'+str(max_zone_counter) + '\n')
                    except:#exception handling, both rate limit and search limit
                        print('exception raised, waiting 15 minutes')
                        print('(until:', dt.datetime.now()+dt.timedelta(minutes=15), ')')
                        time.sleep(900)
                os.chdir(dir_pre_zone)

        os.chdir(dir_pre_group)

if __name__ == "__main__":
    main()
