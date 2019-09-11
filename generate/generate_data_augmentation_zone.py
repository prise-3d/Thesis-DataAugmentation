# main imports
import os, sys
import argparse
import pickle

# image processing imports
from PIL import Image

from ipfml.processing import transform, segmentation
from ipfml import utils

# modules imports
sys.path.insert(0, '') # trick to enable import of main folder module

import custom_config as cfg
from modules.utils import data as dt

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

    args = parser.parse_args()
    
    p_data   = args.data
    p_scene  = args.scene
    p_n      = args.n

    # load data extracted by zones
    fileObject = open(p_data, 'rb')  
    scenes_data = pickle.load(fileObject) 

    scene_data = scenes_data[p_scene]
    # get scenes list
    scenes = os.listdir(path)

    # remove min max file from scenes folder
    scenes = [s for s in scenes if min_max_filename not in s]

        # go ahead each scenes
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


if __name__== "__main__":
    main()