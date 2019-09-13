# main imports
import sys, os, argparse
import math
import numpy as np
import pickle
import time

# processing imports
import matplotlib.pyplot as plt
import scipy.stats as stats

# modules imports
sys.path.insert(0, '') # trick to enable import of main folder module

import custom_config as cfg
import utils as utils_functions

# variables
data_expe_folder          = cfg.data_expe_folder
position_file_pattern     = cfg.position_file_pattern
click_line_pattern        = cfg.click_line_pattern

min_x                     = cfg.min_x_coordinate
min_y                     = cfg.min_y_coordinate


def main():

    parser = argparse.ArgumentParser(description="Compute expe data into output file")

    parser.add_argument('--output', type=str, help="output folder expected", required=True)
    parser.add_argument('--n', type=int, help="number of first clicks per zone wished per user")

    args = parser.parse_args()

    p_output   = args.output
    p_n        = args.n

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
        scene_name          = ""

        # open pos file and extract click information 
        with open(pos_filepath, 'r') as f:

            # for each subject check `p_n` on each zone
            zones_filled = {}

            # first init
            for zone_index in cfg.zones_indices:
                zones_filled[zone_index] = 0

            for line in f.readlines():
                
                if click_line_pattern in line and scene_name in cfg.scenes_names:
                    
                    x, y = utils_functions.extract_click_coordinate(line)
         
                    p_x = x - min_x
                    p_y = y - min_y

                    # only accept valid coordinates
                    if utils_functions.check_coordinates(p_x, p_y):

                        # TODO : need to reverse `y` axis for correct zone index (zone 0 on from top left)
                        zone_index = utils_functions.get_zone_index(p_x, p_y)

                        plt.scatter([p_x], [p_y])
                        plt.show()

                        time.sleep(2)

                        # check number of points saved for this specific zone
                        # add only if wished
                        if zones_filled[zone_index] < p_n:
                            scenes[scene_name][zone_index]['x'].append(p_x)
                            scenes[scene_name][zone_index]['y'].append(p_y)
                            zones_filled[zone_index] += 1
                
                elif click_line_pattern not in line:
                    path_scene = line

                if previous_path_scene != path_scene:

                    previous_path_scene = path_scene
                    new_scene = True
                    scene_name = path_scene.split('/')[4]

                    if scene_name in cfg.scenes_names:
                        number_of_scenes += 1

                    # reinit for each scene
                    for zone_index in cfg.zones_indices:
                        zones_filled[zone_index] = 0

                else:
                    new_scene = False

    filepath = os.path.join(cfg.extracted_data_folder, p_output)

    if not os.path.exists(cfg.extracted_data_folder):
        os.makedirs(cfg.extracted_data_folder)

    with open(filepath, 'wb') as f:
        pickle.dump(scenes, f)

    print('Data object are saved into', filepath)

if __name__== "__main__":
    main()