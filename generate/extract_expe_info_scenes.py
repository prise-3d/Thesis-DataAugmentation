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
import utils as utils_functions

# variables
data_expe_folder          = cfg.data_expe_folder
position_file_pattern     = cfg.position_file_pattern
click_line_pattern        = cfg.click_line_pattern

min_x                     = cfg.min_x_coordinate
min_y                     = cfg.min_y_coordinate


def main():

    parser = argparse.ArgumentParser(description="Compute expe data into output file")

    parser.add_argument('--n', type=int, help="`n` first clicks", required=True)
    parser.add_argument('--output', type=str, help="output folder expected", required=True)

    args = parser.parse_args()

    p_n        = args.n
    p_output   = args.output

    # list all folders
    subjects = os.listdir(data_expe_folder)

    print('Number of subjects', len(subjects))

    # initiate list which will contains `n` first clicks (if exists) on zone for each subject on each scene
    scenes = {}

    for scene in cfg.scenes_names:
        
        scenes[scene] = {}
        # construct for each scene
        scenes[scene]['x'] = []
        scenes[scene]['y'] = []
        
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
            
            points_x = []
            points_y = []

            for line in f.readlines():
                
                if click_line_pattern in line and scene_name in cfg.scenes_names:
                    
                    x, y = utils_functions.extract_click_coordinate(line)

                    p_x = x - min_x
                    p_y = y - min_y
                    
                    # only accept valid coordinates
                    if utils_functions.check_coordinates(p_x, p_y):
                        
                        if counter < p_n:
                            scenes[scene_name]['x'].append(p_x)
                            scenes[scene_name]['y'].append(p_y)
                            counter += 1
                
                elif click_line_pattern not in line:
                    path_scene = line

                if previous_path_scene != path_scene:

                    if previous_path_scene != "":
                        pass
                        #plt.title(subject + ' - ' + scene_name)
                        #plt.scatter(points_x, points_y)
                        #plt.show()

                    previous_path_scene = path_scene
                    new_scene = True
                    scene_name = path_scene.split('/')[4]

                    if scene_name in cfg.scenes_names:
                        number_of_scenes += 1

                else:
                    new_scene = False

                if new_scene:
                    counter = 0
    
    filepath = os.path.join(cfg.extracted_data_folder, p_output)

    if not os.path.exists(cfg.extracted_data_folder):
        os.makedirs(cfg.extracted_data_folder)

    # save information about scenes
    with open(filepath, 'wb') as f:
        pickle.dump(scenes, f)

    print('Data object are saved into', filepath)

if __name__== "__main__":
    main()