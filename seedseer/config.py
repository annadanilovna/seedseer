"""Config for seedseer."""

# pathing config
TRAINING_DATA_PATH = "res/training_data"
SEED_DATA_PATH = "res/seed_data"

# cryptocurrency and/or wallet's wordlist for seed generation
WORD_LIST = "res/word_list.txt"

# fonts to generate training data with. should be truetype (ttf)
# fonts unless you want to modify the source code (which wouldn't be hard.)
#
FONTS = ["res/Lato-SemiBold.ttf"]
# "lbb": "res/Lato-Bold.ttf",
# "lmm": "res/Lato-Medium.ttf",
# "lrg": "res/Lato-Regular.ttf",

# in pixels, default 1-5 with incr 1 = 5 steps
#
# BLURS = ["BoxBlur", "GaussianBlur"]   : types of blur to use (see PIL docs)
# BLUR_RADIUS_MIN = 1                   : min radius for blurs
# BLUR_RADIUS_MAX = 5                   : max radius for blurs
# BLUR_RADIUS_INCREMENT = 1             : increment between each steps
#
# so for each image by default 2 blur types and 5 steps will yield 10 images.
#
BLURS = ["BoxBlur", "GaussianBlur"]
BLUR_RADIUS_MIN = 1
BLUR_RADIUS_MAX = 5
BLUR_RADIUS_INCREMENT = 1

# rotation variation
#
# units in degrees.
#
# ROTATION_MIN = -4         : min rotation
# ROTATION_MAX = 4          : max rotation
# ROTATION_INCREMENT = .5   : amount of space between each step
#
# so by default, the generator will generate all permutations going from
# 4 degrees ccw to 4 degrees cw in increments of 0.5 degrees yielding
# 8 permutations for each iteration.
#
ROTATION_MIN = -4
ROTATION_MAX = 4
ROTATION_INCREMENT = .5

# training data settings
#
# TD_WIDTH = 100            : image width
# TD_HEIGHT = 50            : image height
# TD_FONT_SIZE = 16         : text font size
# TD_DPI = 72               : image dpi
# TD_X_OFFSET = 5           : x offset for text placement (from left top)
# TD_Y_OFFSET = 14          : y offset for text placement (from top left
#                           :      defines top left corner of text)
# TD_BG = "#a0a0a0"         : background color for iages
#
TD_WIDTH = 100
TD_HEIGHT = 50
TD_FONT_SIZE = 16
TD_DPI = 72
TD_X_OFFSET = 5
TD_Y_OFFSET = 14
TD_BG = "#a0a0a0"


TF_BATCH_SIZE = 32
TF_IMG_WIDTH = TD_WIDTH
TF_IMG_HEIGHT = TD_HEIGHT
TF_VALIDATION_SPLIT = 0.2
TF_SEED = 123

TF_CHECKPOINT_PATH = "res/tf/checkpoints"
TF_DS_INIT_CP = "dsinitcp.ckpt"
TF_MODEL_PATH = "res/tf/models"
TF_MODEL_FILE = "seedseer_model"

# 1626 words
# * 8 rotation options
# * 5 blur options
# * 1 font  40*1626 = 52,032 total training images
