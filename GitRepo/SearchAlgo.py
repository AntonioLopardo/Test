import TweetSearch as ts
import os
import time
import pandas as pd
import datetime as dt
import load_utilies as lu
import sys

def progress(count, total, status=''):
    print(' in progress ')
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def main():
    
    if len(sys.argv) is 1:
    
        data_path = input('Where do you want to keep the data:')
    
    else:
        data_path = sys.argv[1] 

    search_groups_dict,search_groups_list, regions_list, coor_dict = lu.load_data_from_path_search(data_path)
    print('loaded_data')

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
                    print(zone,'Already in\n')
                else:
                    os.mkdir(zone_path)
        os.chdir(dir_pre_search_group)

    #print(regions_list[:])

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
                        total = 901
                        i = 1
                        while i < total:
                            progress(i, total, status='seconds elapsed')
                            time.sleep(1)  # emulating long-playing job
                            i += 1

                os.chdir(dir_pre_zone)

        os.chdir(dir_pre_group)

if __name__ == "__main__":
    main()
