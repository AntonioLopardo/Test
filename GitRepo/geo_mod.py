import json
import subprocess
import os

def map_generator(exact_regions_list, search_groups_list, map, labels_feature, dict, script_cwd):

    with open(map,"r") as f: #Loading data
        data = json.load(f)

    OldData = data

    for feature in data["features"]: #looping through the Regions
        feature["properties"]["FAV"] = "Nope" #Addind the FAV (favourite) feature in the dict
        print(feature["properties"][labels_feature])
        if feature["properties"][labels_feature] in exact_regions_list:
            feature["properties"]["FAV"] = search_groups_list[0] #setting the standard FAV to the first search_group
            feature["properties"]["FAVadv"] = str(0.0) #setting the standard FAVadv to 0

            for search_group in search_groups_list: #looping through the search_groups
                feature["properties"][search_group] = str(dict[search_group][feature["properties"][labels_feature]]) #Setting the value of pop in the Region in the GEOJSON file
                if dict[feature["properties"]["FAV"]][feature["properties"][labels_feature]]<dict[search_group][feature["properties"][labels_feature]]: #checking if the current search_group is more pop than the current FAV
                    feature["properties"]["FAVadv"] = str("{0:.3f}".format(dict[search_group][feature["properties"][labels_feature]]-
                                                         dict[feature["properties"]["FAV"]][feature["properties"][labels_feature]])) #Setting the advantage based on the difference between current FAV and newFAV
                    feature["properties"]["FAV"] = search_group

        print (feature["properties"][labels_feature])

    new_map = 'new_' + map #directory for the new GEOJSON map

    with open(new_map, "w+") as fw: #writing the new GEOJSON map
        json.dump(data, fw)

    exact_dir_mbtiles = new_map.split('.')[0] + '.mbtiles' #directory of actual map usable in Mapbox as a .mbtiles

    
    mbtiles_journal_files = [mbj_file for mbj_file in os.listdir(os.getcwd()) if mbj_file.endswith('.mbtiles-journal')]

    for file in mbtiles_journal_files: #eliminating the the .mbtiles-journals that don't allow for a new map to be made
        os.remove(file)
        
    mbtiles_files = [mb_file for mb_file in os.listdir(os.getcwd()) if mb_file.endswith('.mbtiles')]
    
    for file in mbtiles_files: #eliminating the the .mbtiles that don't allow for a new map to be made
        os.remove(file)
    
    subprocess.check_call(["tippecanoe",
                            "-o",
                            exact_dir_mbtiles,
                            "-Z",
                            "4",
                            "-z",
                            "10",
                            new_map]) #running bash tippecanoe to reformat the map in order to be directly usable in Mapbox

    mbtiles_journal_files = [mbj_file for mbj_file in os.listdir(os.getcwd()) if mbj_file.endswith('.mbtiles-journal')]

    for file in mbtiles_journal_files: #eliminating the the .mbtiles-journals that don't allow for a new map to be made
        os.remove(file)

    os.remove(new_map) #eliminating the GEOJSON map in order to leave the data directory as it was found




    return
