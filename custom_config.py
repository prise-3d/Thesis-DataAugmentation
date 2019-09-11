from modules.config.global_config import *

# store all variables from global config
context_vars = vars()

# folders
data_expe_folder                = 'data_expe'
data_augmented_filename         = 'augmented_dataset.csv'

# variables
image_scene_size                = (800, 800)
image_zone_size                 = (200, 200)
possible_point_zone             = tuple(np.asarray(image_scene_size) - np.array(image_zone_size))

position_file_pattern           = 'pos'
click_line_pattern              = 'souris'

## normalization_choices           = ['svd', 'svdn', 'svdne']

# parameters