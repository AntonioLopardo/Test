import json
import sentiment_mod as s
import os
import GeoJSONCameraPlur as gj
import requests
import json
import random

GlobalCounter = 0

def loadCOLLlist(filename):
    Collegi_list = []
    with open(filename) as f:
        for line in f.readlines():
            zone_list = [x.strip() for x in line.split(' ')]
            Collegi_list.append(zone_list)

    return (Collegi_list)

def popFunc(filenames):
    global GlobalCounter
    tweets_data = []
    pop = 0
    numtweets = 0
    normpop = 0
    for file in filenames:
        #print(file)
        with open(file, 'r') as f:
            tweets_data_infile = []
            for line in f:
                    tweets_data_infile.append(json.loads(line))
        for record in tweets_data_infile:
            sent_value, conf = s.sentiment(record['text'])
            if conf*100>=80:
                if random.uniform(0,1) < 0.0005:
                    print(record['text'])
                    print(sent_value, conf)
                numtweets += 1
                GlobalCounter +=1
                if sent_value>0:
                    pop +=1
                    #if random.uniform(0,1) < 0.001:
                     #   print('PoP:' + str(pop))
                      #  print('numtweets:' + str(numtweets))
    try:
        normpop = pop/numtweets
        print('\n' + 'Total number of tweets:' + str(numtweets) + '\n')
        print('NormPop:' + str(normpop)+ '\n\n\n')

    except:
        print('0 tweet brah')

    return normpop

pop_dict = {}
pop_dict['Destra'] = {}
pop_dict['Sinistra'] = {}
pop_dict['M5S'] = {}
Collegi_list = loadCOLLlist('CameraPlur/LIST_CAMERA_PLUR_2017.csv')
search_groups_list = ['Destra', 'Sinistra', 'M5S']

cur_dir = os.getcwd()
dir_string = cur_dir + '/' +'CameraPlur'
os.chdir(dir_string)



for search_group in search_groups_list:
    dir_pre_group = os.getcwd()
    dir_string = dir_pre_group + '/' + search_group
    os.chdir(dir_string)
    for Collegio in Collegi_list:
        nome_collegio = Collegio[0][:-2]
        json_files = []
        for zona in Collegio:
            dir_pre_collegio = os.getcwd()
            dir_string = dir_pre_collegio + '/' + zona
            os.chdir(dir_string)
            listdir = os.listdir()
            for folder in listdir:
                #print(folder)
                dir_pre_folder = os.getcwd()
                dir_string = dir_pre_folder + '/' + folder
                os.chdir(dir_string)
                new_json_files = [pos_json for pos_json in os.listdir(os.getcwd()) if pos_json.endswith('.json')]
                new_json_files = [os.getcwd()+ '/' + json_file for json_file in new_json_files]
                json_files.extend(new_json_files)
                os.chdir(dir_pre_folder)
            os.chdir(dir_pre_collegio)
        pop_dict[search_group][nome_collegio] = popFunc(json_files)
        print(nome_collegio + '-' + search_group + ':' + str(pop_dict[search_group][nome_collegio]))
    os.chdir(dir_pre_group)

os.chdir(cur_dir)
Exact_Collegi_list = []

for Collegio in Collegi_list:
    Exact_Collegi_list.append(Collegio[0][:-2])


for Collegio in Exact_Collegi_list:
    nome_collegio = Collegio
    print(nome_collegio)
    for search_group in search_groups_list:
        print('   ' + search_group + ':' + str(pop_dict[search_group][nome_collegio]))
    print('\n')
map = '/home/antoniolopardo/Desktop/myRNN/mySentRNN_v0.02/CameraPlur/COLL_CAMERA_PLUR_2017.geojson'

gj.map_generator(Exact_Collegi_list,search_groups_list,map,pop_dict)
print('\n\n' + str(GlobalCounter))

