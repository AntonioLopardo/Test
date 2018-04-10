'''
pop_general computes the popularity of every search group in each region
producing a popularity dictionary sent to ge_mod to create the folium colored map
'''
import os
import json
import random
import sent_mod as s
import geo_mod as gj
import load_utilies as lu
import sys

global_counter = 0 #Global Counter to print the number of tweets actually used during the analysis

def compute_pop(filenames): #Compute the popularity of a single search group in a single region given a list of file
    global global_counter
    tweets_data = []
    pop = 0 # number of positive tweets
    num_tweets = 0 # number of tweets
    normpop = 0 # pop/num_tweets
    for file in filenames:
        #print(file)
        with open(file, 'r') as f:
            tweets_data_infile = []
            for line in f:
                    tweets_data_infile.append(json.loads(line))
        for record in tweets_data_infile:
            sent_value, conf = s.sentiment(record['text']) #Computing the sentiment and confidence through sentiment_mod
            if conf*100>=80:
                if random.uniform(0,1) < 0.0005:
                    print(record['text'])
                    print(sent_value, conf)
                num_tweets += 1 # increasing the number of tweets annalyzed
                global_counter +=1
                if sent_value>0:
                    pop +=1 # increasing the number of positive tweets annalyzed

    try:
        normpop = pop/num_tweets
        print('\n' + 'Total number of tweets:' + str(num_tweets) + '\n')
        print('NormPop:' + str(normpop)+ '\n\n\n')

    except:
        print('0 tweet brah') #handling the case in which no tweets were found in the files
        normpop = 0
    return normpop

def main():

    script_cwd = os.getcwd()
    
    if len(sys.argv) is 1:

        data_path = input("""Path to data,\n
    the directory should contain a list_REGIONS csv\n
    a MAP geojson\n
    and the data divided by search_group in different folders\n
    and nothing esle, \n
    no joke don\'t put anything else: """)

    else:
        data_path = sys.argv[1]

    search_groups_dict,search_groups_list,regions_list, map, labels_feature = lu.load_data_from_path_pop(data_path)

    data_dir = os.getcwd()

    pop_dict = {} #Dictionary of the popularity dictionaries of the search_groups

    for search_group in search_groups_list:
        pop_dict[search_group] = {} #Dictionary of the popularity of the search_group for every region

    for search_group in search_groups_list: #loop through the search groups (parties)
        dir_pre_group = os.getcwd()
        dir_string = dir_pre_group + '/' + search_group
        os.chdir(dir_string) #cd into the search_group directory

        for region in regions_list:
            #print(region)
            name_region = region[0][:-2] #save the name of the region removing the subsection in the first zone
            json_files = [] #list of the files in every zone of the region and every search terms

            for zone in region: # loop through the regions
                dir_pre_region = os.getcwd()
                dir_string = dir_pre_region + '/' + zone
                os.chdir(dir_string) #cd into the zone directory
                listdir = os.listdir()

                for folder in listdir: # loop through the different search terms
                    #print(folder)
                    dir_pre_folder = os.getcwd()
                    dir_string = dir_pre_folder + '/' + folder
                    os.chdir(dir_string)
                    new_json_files = [pos_json for pos_json in os.listdir(os.getcwd()) if pos_json.endswith('.json')] #adding only .json files
                    new_json_files = [os.getcwd()+ '/' + json_file for json_file in new_json_files]
                    json_files.extend(new_json_files)
                    os.chdir(dir_pre_folder)

                os.chdir(dir_pre_region)

            pop_dict[search_group][name_region] = compute_pop(json_files) #Computing the popularity of the search_group in the Region
            print(name_region + '-' + search_group + ':' + str(pop_dict[search_group][name_region]))

        os.chdir(dir_pre_group)

    os.chdir(data_dir)
    exact_regions_list = []

    for region in regions_list: #Compose the list of the names of Regions removing the subsections
        exact_regions_list.append(region[0][:-2])


    for region in exact_regions_list: #print the contents of the dictonary to pass to the map generator
        name_region = region
        print(name_region)
        for search_group in search_groups_list:
            print('   ' + search_group + ':' + str(pop_dict[search_group][name_region]))
        print('\n')

    gj.map_generator(exact_regions_list,
                     search_groups_list,
                     map,
                     labels_feature,
                     pop_dict,
                     script_cwd) #sending the list and dict to the map generator to produce a new map

    print('\n\n' + str(global_counter))

if __name__ == "__main__":
    main()
