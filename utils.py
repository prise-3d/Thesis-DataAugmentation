# main imports
import sys, math, os

# processing imports
import matplotlib.pyplot as plt
from PIL import Image

# modules imports
sys.path.insert(0, '') # trick to enable import of main folder module

import custom_config as cfg

min_x = 100
min_y = 100

# utils variables
zone_width, zone_height   = cfg.image_zone_size
scene_width, scene_height = cfg.image_scene_size
nb_x_parts                = math.floor(scene_width / zone_width)

def get_zone_index(p_x, p_y):

    zone_index = math.floor(p_x / zone_width) + math.floor(p_y / zone_height) * nb_x_parts

    return zone_index


def check_coordinates(p_x, p_y):

    if p_x < 0 or p_y < 0:
        return False
        
    if p_x >= scene_width or p_y >= scene_height:
        return False
    
    return True


def extract_click_coordinate(line):

    data = line.split(' : ')[1].split(',')

    p_x, p_y = (int(data[0]), int(data[1]))

    return (p_x, p_y)


def save_img_plot(scene_name, x_points, y_points, title, img_path):

    folder_scene = os.path.join(cfg.dataset_path, scene_name)

    images = [img for img in os.listdir(folder_scene) if '.png' in img]
    images = sorted(images)

    first_image_path = os.path.join(folder_scene, images[0])
    img = Image.open(first_image_path)

    plt.rcParams["figure.figsize"] = (20, 20)

    # Save here data information about subject
    plt.title(title, fontsize=30)
    plt.imshow(img)
    plt.scatter(x_points, y_points, color='red')

    for x_i, x in enumerate(cfg.zone_coodinates):
        plt.plot([x_i * 200, x_i * 200], [0, 800], color='blue')

    for y_i, y in enumerate(cfg.zone_coodinates):
        plt.plot([0, 800], [y_i * 200, y_i * 200], color='blue')

    plt.axis('off')
    plt.savefig(img_path, dpi=100)