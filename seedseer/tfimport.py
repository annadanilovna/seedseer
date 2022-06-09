"""Import data into TF."""

import pathlib

import tensorflow as tf

from . import config


def tfimport():
    root = pathlib.Path(config.TRAINING_DATA_PATH)
    for item in root.glob("*"):
        sub_root = pathlib.Path(item.absolute())
        for sub_item in sub_root.glob("*"):
            print(sub_item.name)
