import os
import load_utilies as lu

def reg_coor_write(list_csv_files):
    alphabet = list(string.ascii_lowercase)
    coor_list = []
    for file in list_csv_files:

        with open(file, 'r') as f:
            reader = csv.reader(f)
            data_list = list(reader)

        alpha_counter = 0
        for i in range(0,len(data_list[0]),3):
            zone_name = file.split('.')[0] + '-' + alphabet[alpha_counter]
            alpha_counter += 1
            lat = data_list[0][i]
            lng = data_list[0][i+1]
            radius = data_list[0][i+2].split('.')[0][:2]+'.'+data_list[0][i+2].split('.')[0][2:]
            coor_data = lat+','+lng+','+radius+'km'
            coor_list_entry = [zone_name,coor_data]
            coor_list.append(coor_list_entry)

    with open('COOR_ZONES.csv', 'w') as f:
        writer = csv.writer(f,delimiter=' ')
        writer.writerow(['ZONES','COOR'])
        for coor_list_entry in coor_list:
            writer.writerow(coor_list_entry)

def reg_list_write(list_csv_files):
    alphabet = list(string.ascii_lowercase)
    reg_list = []
    for file in list_csv_files:

        with open(file, 'r') as f:
            reader = csv.reader(f)
            data_list = list(reader)

        zones_number = int(len(data_list[0])/3)

        zones_list = []

        for i in range(0,zones_number):
            zone_name = file.split('.')[0] + '-' + alphabet[i]
            zones_list.append(zone_name)
        reg_list.append(zones_list)

    with open('LIST_ZONES.csv', 'w') as f:
        writer = csv.writer(f)
        for region in reg_list[:]:
            writer.writerow(region)

def main():

    if len(sys.argv) is 1:

        data_path = input('Where do you want to save the files:')

    else:
        data_path = sys.argv[1]

    cur_dir = os.getcwd()
    os.chdir(dat_path)
    coor_csv_files = [csv_file for csv_file in os.listdir(os.getcwd()) if csv_file.endswith('.csv')]
    os.chdir(cur_dir)

    reg_coor_write(coor_csv_files)
    reg_list_write(coor_csv_files)

    map_dir,_ = lu.load_map_file()

    with open('config.csv', 'w') as f:
        writer = csv.writer(f,delimiter=' ')
        writer.writerow(['ZONES','COOR'])
        writer.writerow(['regions_list','LIST_ZONES.csv'])
        writer.writerow(['coor_dict','COOR_ZONES.csv'])
        writer.writerow(['map',map_dir])
