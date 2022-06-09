"""Config for seedseer."""


# Cryptocurrency and/or wallet's wordlist for seed generation
WORD_LIST = "res/word_list.txt"

# Base path for training data
TRAINING_DATA_PATH = "res/training_data"
SEED_DATA_PATH = "res/seed_data"

FONTS = ["res/Lato-SemiBold.ttf"]
# "lbb": "res/Lato-Bold.ttf",
# "lmm": "res/Lato-Medium.ttf",
# "lrg": "res/Lato-Regular.ttf",

BLURS = ["BoxBlur", "GaussianBlur"]

# in pixels, default 1-5 with incr 1 = 5 steps
BLUR_RADIUS_MIN = 1
BLUR_RADIUS_MAX = 5
BLUR_RADIUS_INCREMENT = 1

# in degrees, default 4 degrees in .25 steps = 8 options
ROTATION_MIN = -10
ROTATION_MAX = 10
ROTATION_INCREMENT = .5

# 1626 words
# * 8 rotation options
# * 5 blur options
# * 1 font  40*1626 = 52,032 total training images
