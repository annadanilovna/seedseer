#!/usr/bin/env python


import argparse
import logging

# import recover
# import train
from .generate import generate


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
                        filename="seedseer.log")

    parser = argparse.ArgumentParser(description="ai seed recovery")
    parser.add_argument("action")

    args = parser.parse_args()
    if args.action == "gen":
        generate()
    elif args.action == "train":
        # train.train()
        pass
    elif args.action == "recover":
        # recover.recover()
        pass
    else:
        raise Exception("Invalid action requested.")
