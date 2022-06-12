"""Config for seedseer."""

# pathing config
TRAINING_DATA_PATH = "res/training_data"
SEED_DATA_PATH = "res/seed_data"

# tensorflow. saved data path. checkpoint and training model paths.
TF_CHECKPOINT_PATH = "res/tf/checkpoints"
TF_MODEL_PATH = "res/tf/models"
TF_MODEL_FILE = "seedseer_model"

# the app will check if these paths exist and create them if they don't prior to starting.
CHECK_PATHS = [TF_CHECKPOINT_PATH, TF_MODEL_PATH,
               f"{TF_MODEL_PATH}/{TF_MODEL_FILE}",
               TRAINING_DATA_PATH, SEED_DATA_PATH]

# cryptocurrency and/or wallet's wordlist for seed generation
WORD_LIST = "res/word_list.txt"
LOG_FILE = "seedseer.log"

# fonts to generate training data with. should be truetype (ttf)
FONT = "res/Lato-SemiBold.ttf"
FONT_SIZE = 16
FONT_COLOR = "#000000"

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

# "#090909", "#929292",
SPRITE_BGS = ["#a0a0a0", "#a3a3a3",
              "#a8a8a8", "#c0c0c0",
              "#c6c6c6", "#cacaca",
              "#cccccc", "#d0d0d0",
              "#dadada", "#dbdbdb",
              "#d9d9d9", "#e2e2e2",
              "#eeeeee"]

TL_TIMING_DIV = 1000

TEXT_PADDING = 5
TEXT_X_OFFSET = TEXT_PADDING
TEXT_Y_OFFSET = TEXT_PADDING  # calc this at runtime since diff for diff sizes

# TensorFlow model config
TF_BATCH_SIZE = 32
TF_IMG_WIDTH = SPRITE_WIDTH
TF_IMG_HEIGHT = SPRITE_HEIGHT
TF_VALIDATION_SPLIT = 0.2
TF_SEED = 123
