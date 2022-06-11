"""Config for seedseer."""

# pathing config
TRAINING_DATA_PATH = "res/training_data"
SEED_DATA_PATH = "res/seed_data"

# cryptocurrency and/or wallet's wordlist for seed generation
WORD_LIST = "res/word_list.txt"
LOG_FILE = "seedeer.log"

# fonts to generate training data with. should be truetype (ttf)
# fonts unless you want to modify the source code (which wouldn't be hard.)
#
FONTS = ["res/Lato-SemiBold.ttf"]
FONT_SIZES = [16]
FONT_COLORS = ["#000000"]

BLURS = ["BoxBlur", "GaussianBlur"]
BLUR_RADIUS_MIN = 1
BLUR_RADIUS_MAX = 5
BLUR_RADIUS_INCREMENT = 1

ROTATION_MIN = -4
ROTATION_MAX = 4
ROTATION_INCREMENT = .5

SPRITE_COLORSPACE = "L"
SPRITE_WIDTH = 100
SPRITE_HEIGHT = 50
SPRITE_DPI = 72
SPRITE_BGS = ["#a0a0a0"]

TEXT_PADDING = 5
TEXT_X_OFFSET = TEXT_PADDING
TEXT_Y_OFFSET = TEXT_PADDING  # calc this at runtime since diff for diff sizes
TF_BATCH_SIZE = 32
TF_IMG_WIDTH = SPRITE_WIDTH
TF_IMG_HEIGHT = SPRITE_HEIGHT
TF_VALIDATION_SPLIT = 0.2
TF_SEED = 123

TF_CHECKPOINT_PATH = "res/tf/checkpoints"
TF_DS_INIT_CP = "dsinitcp.ckpt"
TF_MODEL_PATH = "res/tf/models"
TF_MODEL_FILE = "seedseer_model"

CHECK_PATHS = [TF_CHECKPOINT_PATH, TF_MODEL_PATH,
               f"{TF_MODEL_PATH}/{TF_MODEL_FILE}",
               TRAINING_DATA_PATH, SEED_DATA_PATH]

# 1626 words
# * 8 rotation options
# * 5 blur options
# * 1 font  40*1626 = 52,032 total training images
