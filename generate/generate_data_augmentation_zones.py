# main imports
import os, sys
import argparse
import pickle
import random
import numpy as np
import math

# image processing imports
from PIL import Image

from ipfml.processing import transform, segmentation
from ipfml import utils

# modules imports
sys.path.insert(0, '') # trick to enable import of main folder module

import custom_config as cfg
from modules.utils import data as dt

import utils as utils_functions

# getting configuration information
zone_folder             = cfg.zone_folder
min_max_filename        = cfg.min_max_filename_extension

# define all scenes values
scenes_list             = cfg.scenes_names
scenes_indexes          = cfg.scenes_indices
path                    = cfg.dataset_path
zones                   = cfg.zones_indices
seuil_expe_filename     = cfg.seuil_expe_filename

output_data_folder      = cfg.output_data_folder

image_scene_size        = cfg.image_scene_size
image_zone_size         = cfg.image_zone_size
possible_point_zone     = cfg.possible_point_zone


def main():

    parser = argparse.ArgumentParser(description="Compute and prepare data augmentation of scenes")

    parser.add_argument('--data', type=str, help="object filename saved using pickle", required=True)
    parser.add_argument('--scene', type=str, help="scene name to display click information", required=True, choices=cfg.scenes_names)
    parser.add_argument('--n', type=int, help="number of clics per zone wished")
    parser.add_argument('--images', type=int, help="number of images (with estimated thresholds) wished by scene")
    parser.add_argument('--output', type=str, help="output file with new thresholds data")

    args = parser.parse_args()
    
    p_data   = args.data
    p_scene  = args.scene
    p_n      = args.n
    p_images = args.images
    p_output = args.output

    # load data extracted by zones
    fileObject = open(p_data, 'rb')  
    scenes_data = pickle.load(fileObject) 

    # get clicks data of specific scene
    scene_data = scenes_data[p_scene]

    # getting image zone size and usefull information
    zone_width, zone_height = image_zone_size
    scene_width, scene_height = image_scene_size
    nb_x_parts = math.floor(scene_width / zone_width)

    # get scenes list
    scenes = os.listdir(path)

    # remove min max file from scenes folder
    scenes = [s for s in scenes if min_max_filename not in s]

    # go ahead each scenes in order to get threshold
    for folder_scene in scenes:

        scene_path = os.path.join(path, folder_scene)

        # construct each zones folder name
        zones_folder = []
        zones_threshold = []

        # get zones list info
        for index in zones:
            index_str = str(index)
            if len(index_str) < 2:
                index_str = "0" + index_str

            current_zone = "zone"+index_str
            zones_folder.append(current_zone)

            zone_path = os.path.join(scene_path, current_zone)

            with open(os.path.join(zone_path, seuil_expe_filename)) as f:
                zones_threshold.append(int(f.readline()))

        # generate a certain number of images
        for i in range(p_images):
            
            ###########################################
            # Compute weighted threshold if necessary #
            ###########################################           

            ##############################
            # 1. Get random point from possible position
            ##############################
            possible_x, possible_y = possible_point_zone

            p_x, p_y = (random.randrange(possible_x), random.randrange(possible_y))

            ##############################
            # 2. Get zone indices of this point (or only one zone if `%` 200)
            ##############################

            # coordinate of specific zone, hence use threshold of zone
            if p_x % zone_width == 0 and p_y % zone_height == 0:
                    
                zone_index = utils_functions.get_zone_index(p_x, p_y)

                final_threshold = int(zones_threshold[zone_index])
            else:
                # get zone identifiers of this new zones (from endpoints)
                p_top_left = (p_x, p_y)
                p_top_right = (p_x + zone_width, p_y)
                p_bottom_right = (p_x + zone_width, p_y + zone_height)
                p_bottom_left = (p_x, p_y + zone_height)

                points = [p_top_left, p_top_right, p_bottom_right, p_bottom_left]

                p_zones_indices = []
                
                # for each points get threshold information
                for p in points:
                    x, y = p

                    zone_index = utils_functions.get_zone_index(x, y)
                    p_zones_indices.append(zone_index)

                # 2.3. Compute area of intersected zones (and weights)
                # get proportions of pixels of img into each zone
                overlaps = []

                p_x_max = p_x + zone_width
                p_y_max = p_y + zone_height

                for index, zone_index in enumerate(p_zones_indices):
                    x_zone = (zone_index % nb_x_parts) * zone_width
                    y_zone = (math.floor(zone_index / nb_x_parts)) * zone_height

                    x_max_zone = x_zone + zone_width
                    y_max_zone = y_zone + zone_height

                    # computation of overlap
                    # x_overlap = max(0, min(rect1.right, rect2.right) - max(rect1.left, rect2.left))
                    # y_overlap = max(0, min(rect1.bottom, rect2.bottom) - max(rect1.top, rect2.top))
                    x_overlap = max(0, min(x_max_zone, p_x_max) - max(x_zone, p_x))
                    y_overlap = max(0, min(y_max_zone, p_y_max) - max(y_zone, p_y))

                    overlapArea = x_overlap * y_overlap
                    overlaps.append(overlapArea)

                overlapSum = sum(overlaps)

                # area weights are saved into proportions
                proportions = [item / overlapSum for item in overlaps]

                # 2.4. Count number of clicks present into each zones intersected (and weights)
                

                # 2.5. Compute final threshold of `x` and `y` using `3` and `4` steps
                p_thresholds = np.array(zones_threshold)[p_zones_indices]

            # 3. Save this new entry into .csv file (scene_name; x; y; threshold)

if __name__== "__main__":
    main()