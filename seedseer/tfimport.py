"""Import data into TF."""

import os
import pathlib

import tensorflow as tf
import numpy as np

from . import config


np.set_printoptions(precision=4)


def process_path(file_path):
    label = tf.strings.split(file_path, os.sep)[-2]
    return tf.io.read_file(file_path), label


def tfimport():

    batch_size = 32
    img_width = 100
    img_height = 50

    root = pathlib.Path(config.TRAINING_DATA_PATH)

    # It's good practice to use a validation split when developing your model. # You will use 80% of the images for training and 20% for validation.

    train_ds = tf.keras.utils.image_dataset_from_directory(
        config.TRAINING_DATA_PATH,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    # Found 3670 files belonging to 5 classes.
    # Using 2936 files for training.

    val_ds = tf.keras.utils.image_dataset_from_directory(
        config.TRAINING_DATA_PATH,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    # Found 3670 files belonging to 5 classes.
    # Using 734 files for validation.

    # You can find the class names in the class_names attribute on these
    # datasets.

    class_names = train_ds.class_names
    print(class_names)
