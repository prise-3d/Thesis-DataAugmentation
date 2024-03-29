# main imports
import os, sys
import argparse
import pickle
import numpy as np

# processing imports
import matplotlib.pyplot as plt

# modules imports
sys.path.insert(0, '') # trick to enable import of main folder module

import custom_config as cfg
from modules.utils import data as dt


def main():

    parser = argparse.ArgumentParser(description="Compute and prepare data augmentation of scenes")

    parser.add_argument('--data', type=str, help="object filename saved using pickle", required=True)
    parser.add_argument('--scene', type=str, help="scene name to display click information", required=True, choices=cfg.scenes_names)

    args = parser.parse_args()
    
    p_data   = args.data
    p_scene  = args.scene

    # load data extracted by zones
    fileObject = open(p_data, 'rb')  
    scenes_data = pickle.load(fileObject) 

    scene_data = scenes_data[p_scene]
    
    # set title and zone axis
    plt.title(p_scene, 'with data :', p_data)

    for x_i, x in enumerate(cfg.zone_coodinates):
        plt.plot([x_i * 200, x_i * 200], [0, 800], color='red')

    for y_i, y in enumerate(cfg.zone_coodinates):
        plt.plot([0, 800], [y_i * 200, y_i * 200], color='red')

    x_points = []
    y_points = []

    for index, zone in scene_data.items():

        x_points = np.append(x_points, zone['x'])
        y_points = np.append(y_points, zone['y'])   

    plt.scatter(x_points, y_points)
    plt.show()


if __name__== "__main__":
    main()