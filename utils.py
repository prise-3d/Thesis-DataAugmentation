# main imports
import sys, math

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

    if p_x < min_x or p_y < min_y:
        return False
        
    if p_x >= min_x + scene_width or p_y >= min_y + scene_height:
        return False
    
    return True


def extract_click_coordinate(line):

    data = line.split(' : ')[1].split(',')

    p_x, p_y = (int(data[0]), int(data[1]))

    return (p_x, p_y)
