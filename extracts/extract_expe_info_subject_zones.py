# main imports
import sys, os, argparse
import math
import numpy as np
import pickle
import time

# processing imports
from PIL import Image

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
image_scene_size          = cfg.image_scene_size
scene_width, scene_height = image_scene_size


def main():

    parser = argparse.ArgumentParser(description="Compute expe data into output file")

    parser.add_argument('--n', type=int, help="`n` first clicks", required=True)
    parser.add_argument('--folder', type=str, help="output folder expected", required=True)
    parser.add_argument('--reverse', type=int, help="reverse or not y axis clicks", default=False)

    args = parser.parse_args()

    p_n        = args.n
    p_folder   = args.folder
    p_reverse  = bool(args.reverse)

    print(p_reverse)

    # list all folders
    subjects = os.listdir(data_expe_folder)

    print('Number of subjects', len(subjects))

    output_folder_path = os.path.join(cfg.media_data_folder, p_folder)

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # keep scene_data in memory
    scenes_data = {}   

    for scene in cfg.scenes_names:
        
        zones_list = {}

        for zone_index in cfg.zones_indices:

            zones_list[zone_index] = {}
            # construct for each scene
            zones_list[zone_index]['x'] = []
            zones_list[zone_index]['y'] = []

        scenes_data[scene] = zones_list

    for _, subject in enumerate(subjects):
        
        subject_folder = os.path.join(data_expe_folder, subject)
        data_files = os.listdir(subject_folder)

        pos_file = [f for f in data_files if position_file_pattern in f][0]
        
        pos_filepath = os.path.join(subject_folder, pos_file)

        previous_path_scene = ""
        path_scene          = ""
        new_scene           = True
        number_of_scenes    = 0
        scene_name          = ""

        print('Extract images clicks of subject', subject)

        # open pos file and extract click information 
        with open(pos_filepath, 'r') as f:

            # for each subject check `p_n` on each zone
            zones_filled = {}
            zones_clicks_of_subject = {}

            for zone_index in cfg.zones_indices:
                zones_filled[zone_index] = 0

                zones_clicks_of_subject[zone_index] = {}
                zones_clicks_of_subject[zone_index]['x'] = []
                zones_clicks_of_subject[zone_index]['y'] = []

            for line in f.readlines():
                
                if click_line_pattern in line and scene_name in cfg.scenes_names:
                    
                    x, y = utils_functions.extract_click_coordinate(line)

                    p_x = x - min_x
                    p_y = y - min_y

                    # only accept valid coordinates (need to substract `x_min` and `y_min` before check)
                    if utils_functions.check_coordinates(p_x, p_y):
                        
                        if p_reverse:
                            # add reversed points here
                            p_y = scene_height - p_y

                        # get zone indice
                        zone_index = utils_functions.get_zone_index(p_x, p_y)

                        # check number of points saved for this specific zone
                        # add only if wished
                        if zones_filled[zone_index] < p_n:

                            zones_clicks_of_subject[zone_index]['x'].append(p_x)
                            zones_clicks_of_subject[zone_index]['y'].append(p_y)
                            zones_filled[zone_index] += 1
                
                elif click_line_pattern not in line:
                    path_scene = line

                if previous_path_scene != path_scene:

                    previous_path_scene = path_scene
                    new_scene = True
                    scene_name = path_scene.split('/')[4]

                    if scene_name in cfg.scenes_names:
                        number_of_scenes += 1

                        if previous_path_scene != "":

                            subject_path = os.path.join(output_folder_path, subject)
                            
                            if not os.path.exists(subject_path):
                                os.makedirs(subject_path)     

                            output_image_name = subject + '_' + scene_name + '_' + str(p_n) + '.png'
                            img_path = os.path.join(subject_path, output_image_name)

                            title = subject + ' - ' + scene_name + ' (' + str(p_n) + ' clicks)'

                            x_points = []
                            y_points = []

                            for zone_index in cfg.zones_indices:
                                # save image plot
                                x_points = x_points + zones_clicks_of_subject[zone_index]['x']
                                y_points = y_points + zones_clicks_of_subject[zone_index]['y']

                            utils_functions.save_img_plot(scene_name, x_points, y_points, title, img_path)

                            # save scene data
                            for i in cfg.zones_indices:
                                scenes_data[scene_name][i]['x'] = scenes_data[scene_name][i]['x'] + x_points
                                scenes_data[scene_name][i]['y'] = scenes_data[scene_name][i]['y'] + y_points

                        # reinit zones list
                        for zone_index in cfg.zones_indices:
                            zones_filled[zone_index] = 0

                            zones_clicks_of_subject[zone_index] = {}
                            zones_clicks_of_subject[zone_index]['x'] = []
                            zones_clicks_of_subject[zone_index]['y'] = []

                else:
                    new_scene = False

    all_path_folder = os.path.join(output_folder_path, cfg.all_subjects_data_folder)

    if not os.path.exists(all_path_folder):
        os.makedirs(all_path_folder)


    print('Merge images clicks of subjects into', all_path_folder)
    for k, v in scenes_data.items():

        current_x_points = [] 
        current_y_points = []

        for i in cfg.zones_indices:
            current_x_points = current_x_points + v[i]['x']
            current_y_points = current_y_points + v[i]['y']

        title = k + ' scene with all subjects (with ' + str(p_n) + ' clicks per subject)'

        img_filename = cfg.all_subjects_data_folder + '_' + k + '_' + str(p_n) + '.png'
        img_path = os.path.join(all_path_folder, img_filename)

        # save figure `all` subjects `p_n` clicks
        utils_functions.save_img_plot(k, current_x_points, current_y_points, title, img_path)


    print('Images are saved into', output_folder_path)
    

if __name__== "__main__":
    main()