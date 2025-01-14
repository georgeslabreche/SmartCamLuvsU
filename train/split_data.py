#!/usr/bin/python

import sys
import os
import shutil
import math

# Check that a valid number of arguments is given.
if len(sys.argv) != 3:
    print('Invalid arguments. Usage e.g.: python3 split_data.py <model_name> 25')
    exit(1)

# The name of the model that is going to be trained.
model_name = sys.argv[1]

# The percentage of data to use as test data.
split_percent = int(sys.argv[2])

# The split modulo to determine the splitting.
split_modulo = math.ceil(100 / split_percent)

# The data directory paths.
all_data_dir_path = 'repo/' + model_name + '/data/all'
training_data_dir_path = 'repo/' + model_name + '/data/training'
test_data_dir_path = 'repo/' + model_name + '/data/test'

# Use this counter to track number of images files.
img_counter = 0

if len(os.listdir(all_data_dir_path)) == 0:
    print('No training directories found. Training data must be grouped into a directory for each target classification label.')
    exit(0)


# Delete all training data label directories that may have been created in a previous split.
training_dirlist = [f for f in os.listdir(training_data_dir_path)]
for d in training_dirlist:
    shutil.rmtree(os.path.join(training_data_dir_path, d), ignore_errors=True)

# Delete all test data label directories that may have been created in a previous split.
test_dirlist = [f for f in os.listdir(test_data_dir_path)]
for d in test_dirlist:
    shutil.rmtree(os.path.join(test_data_dir_path, d), ignore_errors=True)

# Go through all image files to split them as either Training or Test data.
for label_dir_name in os.listdir(all_data_dir_path):
    print("Splitting '" + label_dir_name + "' images into Training or Test datasets...")

    # The label directory path.
    label_dir_path = all_data_dir_path + "/" + label_dir_name

    # Create the label folder in the Training directory, if it doesn't exist already.
    if not os.path.exists(training_data_dir_path + '/' + label_dir_name):
        os.makedirs(training_data_dir_path + '/' + label_dir_name)

    # Create the label folder in the Test directory, if it doesn't exist already.
    if not os.path.exists(test_data_dir_path + '/' + label_dir_name):
        os.makedirs(test_data_dir_path + '/' + label_dir_name)

    # Go through each image in the current label directory and copy it to either the Training or Test directory.
    for image_file in os.listdir(label_dir_path):

        # Use this counter to track the split.
        img_counter = img_counter + 1
        
        # Use module to split files between Training and Test.
        if img_counter % split_modulo == 0:
            # This image is copied to the Test directory.
            shutil.copyfile(label_dir_path + '/' + image_file, test_data_dir_path + '/' + label_dir_name + '/' + image_file)
        else:
            # This image is copied to the Training directory.
            shutil.copyfile(label_dir_path + '/' + image_file, training_data_dir_path + '/' + label_dir_name + '/' + image_file)

# Done.
print('Done')