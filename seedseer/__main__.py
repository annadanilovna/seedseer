#!/usr/bin/env python

import argparse
import logging
import time

# import recover
# import train
# from . import config
from .sprite_generator import SpriteGenerator
from .image_classifier import ImageClassifier


if __name__ == "__main__":

    # set up logging. make sure correct directories exist
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="ai seed recovery")
    parser.add_argument("action")

    args = parser.parse_args()

    start = time.time()
    if args.action == "gen":
        sg = SpriteGenerator()
        sg.generate()
    elif args.action == "train":
        ic = ImageClassifier(load_saved_state=True)
        ic.train()
        ic.save()
        ic.summary()
    elif args.action == "recover":
        ic = ImageClassifier(load_saved_state=True)
        res = ic.classify()
    else:
        raise Exception("Invalid action requested.")

    end = time.time()
    logging.info(f"finished in {round(end - start, 2)} seconds.")
