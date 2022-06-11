#!/usr/bin/env python

import argparse
import logging
import time

# import recover
# import train
from . import config
from .sprite_generator import SpriteGenerator
from .tensor_flow_model import TensorFlowModel


if __name__ == "__main__":

    # set up logging. make sure correct directories exist
    logging.basicConfig(level=logging.DEBUG, filename=config.LOG_FILE)

    parser = argparse.ArgumentParser(description="ai seed recovery")
    parser.add_argument("action")

    args = parser.parse_args()

    start = time.time()
    if args.action == "gen":
        sg = SpriteGenerator()
        sg.generate()
    elif args.action == "train":
        tf = TensorFlowModel()
        tf.train()
        tf.save()
        tf.summary()
    elif args.action == "recover":
        # recover.recover()
        pass
    else:
        raise Exception("Invalid action requested.")
    end = time.time()

    print(f"finished in {round(end - start, 2)} seconds.")
