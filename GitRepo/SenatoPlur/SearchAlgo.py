import TweetSearch as ts
import os
import time
import pandas as pd
import datetime as dt

def loadCOORdata(filename):
    data = pd.read_csv(filename, encoding='latin_1',sep=' ', index_col = 0)
    coor_dict = {}
    coor_dict = data['COOR'].to_dict()
    return coor_dict

def loadCOLLlist(filename):
    Collegi_list = []
    with open(filename) as f:
        for line in f.readlines():
            zone_list = [x.strip() for x in line.split(' ')]
            Collegi_list.append(zone_list)

    return (Collegi_list)

Destra = ['Lega OR ForzaItalia OR Salvini OR matteosalvini OR salvini OR Meloni OR FI OR Berlusconi OR berlusconi']
Sinistra = ['PD OR Renzi OR renzi OR Gentiloni OR gentiloni OR Bonino OR +europa' ]
M5S = ['M5S OR Di Maio OR DiMaio OR Grillo OR DiBattista OR Di Battista OR grillo']

search_groups_dict = {}
search_groups_list = ['Destra', 'Sinistra', 'M5S']
search_groups_dict['Destra'] = Destra
search_groups_dict['Sinistra'] = Sinistra
search_groups_dict['M5S'] = M5S

Collegi_dict = loadCOORdata('COOR_CAMERA_PLUR_2017.csv')
Collegi_list = loadCOLLlist('LIST_CAMERA_PLUR_2017.csv')

print(Collegi_list[:])

min_days_old, max_days_old = 0,1
maxSearch_counter = len(search_groups_list)
Search_counter = 0
for search_group in search_groups_list:
    Search_counter += 1
    dir_pre_group = os.getcwd()
    dir_string = dir_pre_group + '/' + search_group
    os.chdir(dir_string)
    maxCol_counter = len(Collegi_list)
    Col_counter = 0
    for Collegio in Collegi_list:
        Col_counter += 1
        maxZona_counter = len(Collegio)
        Zona_counter = 0
        for zona in Collegio:
            Zona_counter += 1
            dir_pre_zona = os.getcwd()
            dir_string = dir_pre_zona + '/' + zona
            os.chdir(dir_string)
            search_phrases = search_groups_dict[search_group]
            zona_coordinates = Collegi_dict[zona]
            time.sleep(1)
            done = 0
            while done == 0:
                try:
                    ts.dist_search(zona_coordinates,
                                   search_phrases,
                                   min_days_old,
                                   max_days_old)
                    done = 1
                    print('\n'+str(Search_counter)+'/'+str(maxSearch_counter)+ '-' +str(Col_counter)+'/'+str(maxCol_counter) + '-' + str(Zona_counter)+'/'+str(maxZona_counter) + '\n')
                except:
                    print('exception raised, waiting 15 minutes')
                    print('(until:', dt.datetime.now()+dt.timedelta(minutes=15), ')')
                    time.sleep(900)
            os.chdir(dir_pre_zona)
    os.chdir(dir_pre_group)
