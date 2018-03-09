import json
import random as rd

def map_generator(Collegi_list,search_groups,map, dict):

    with open(map,"r") as f:
        data = json.load(f)

    OldData = data

    for feature in data["features"]:
        feature["properties"]["FAV"] = "Nope"
        print(feature["properties"]["CAM17P_DEN"])
        if feature["properties"]["CAM17P_DEN"] in Collegi_list:
            print('dentro if' + feature["properties"]["CAM17P_DEN"])
            feature["properties"]["FAV"] = "Destra"
            feature["properties"]["FAVadv"] = str(0.0)
            for search_group in search_groups:
                feature["properties"][search_group] = str(dict[search_group][feature["properties"]["CAM17P_DEN"]])
                if dict[feature["properties"]["FAV"]][feature["properties"]["CAM17P_DEN"]]<dict[search_group][feature["properties"]["CAM17P_DEN"]]:
                    feature["properties"]["FAVadv"] = str("{0:.2f}".format(dict[search_group][feature["properties"]["CAM17P_DEN"]]-
                                                         dict[feature["properties"]["FAV"]][feature["properties"]["CAM17P_DEN"]]))
                    feature["properties"]["FAV"] = search_group

        print (feature["properties"]["CAM17P_DEN"])

    newmap = 'new' + map.split('/')[-1]
    
    dir_ass = map.split('/')[0]
    for section in map.split('/')[1:-1]:
        dir_ass = dir_ass + '/' + section 
    
    newmap = dir_ass + '/' + newmap
    
    with open(newmap, "w+") as fw:
        json.dump(data, fw)

    return
