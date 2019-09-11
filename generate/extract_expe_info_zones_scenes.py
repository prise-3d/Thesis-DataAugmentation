# main imports
import sys, os, argparse
import math
import numpy as np
import pickle

# processing imports
import matplotlib.pyplot as plt
import scipy.stats as stats

# modules imports
sys.path.insert(0, '') # trick to enable import of main folder module

import custom_config as cfg

# variables
data_expe_folder          = cfg.data_expe_folder
position_file_pattern     = cfg.position_file_pattern
click_line_pattern        = cfg.click_line_pattern

# utils variables
zone_width, zone_height   = cfg.image_zone_size
scene_width, scene_height = cfg.image_scene_size
nb_x_parts                = math.floor(scene_width / zone_width)

min_x = 100
min_y = 100

def get_zone_index(p_x, p_y):

    zone_index = math.floor(p_x / zone_width) + math.floor(p_y / zone_height) * nb_x_parts

    return zone_index


def check_coordinates(p_x, p_y):

    if p_x < min_x or p_y < min_y:
        return False
        
    if p_x >= min_x + scene_width or p_y >= min_y + scene_height:
        return False
    
    return True


def extract_click_coordinate(line):

    data = line.split(' : ')[1].split(',')

    p_x, p_y = (int(data[0]), int(data[1]))

    return (p_x, p_y)


def main():

    parser = argparse.ArgumentParser(description="Compute expe data into output file")

    parser.add_argument('--output', type=str, help="output folder expected", required=True)

    args = parser.parse_args()

    p_output   = args.output

    # list all folders
    subjects = os.listdir(data_expe_folder)

    print('Number of subjects', len(subjects))

    # initiate list which will contains `n` first clicks (if exists) on zone for each subject on each scene
    scenes = {}

    for scene in cfg.scenes_names:
        
        zones_list = {}

        for zone_index in cfg.zones_indices:

            zones_list[zone_index] = {}
            # construct for each scene
            zones_list[zone_index]['x'] = []
            zones_list[zone_index]['y'] = []

        scenes[scene] = zones_list
    
    # for each subjects process data
    for index, subject in enumerate(subjects):
        
        subject_folder = os.path.join(data_expe_folder, subject)
        data_files = os.listdir(subject_folder)

        pos_file = [f for f in data_files if position_file_pattern in f][0]
        
        pos_filepath = os.path.join(subject_folder, pos_file)

        previous_path_scene = ""
        path_scene          = ""
        new_scene           = True
        number_of_scenes    = 0
        counter             = 0
        scene_name          = ""

        # open pos file and extract click information 
        with open(pos_filepath, 'r') as f:

            for line in f.readlines():
                
                if click_line_pattern in line and scene_name in cfg.scenes_names:
                    
                    x, y = extract_click_coordinate(line)

                    # only accept valid coordinates
                    if check_coordinates(x, y):
                        
                        p_x = x - min_x
                        p_y = y - min_y

                        zone_index = get_zone_index(p_x, p_y)

                        scenes[scene_name][zone_index]['x'].append(p_x)
                        scenes[scene_name][zone_index]['y'].append(p_y)
                
                elif click_line_pattern not in line:
                    path_scene = line

                if previous_path_scene != path_scene:

                    previous_path_scene = path_scene
                    new_scene = True
                    scene_name = path_scene.split('/')[4]

                    if scene_name in cfg.scenes_names:
                        number_of_scenes += 1

                else:
                    new_scene = False

                if new_scene:
                    counter = 0

    with open(p_output, 'wb') as f:
        pickle.dump(scenes, f)

if __name__== "__main__":
    main()