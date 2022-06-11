"""Generate training images."""

import logging
import os

from PIL import ImageFont, ImageDraw, Image, ImageFilter

from . import config
from .util import has_method, calc_steps, find_best_sprite_dims
from .config_loader import ConfigLoader


class GeneratorOptions:
    """Data generation options."""

    def __init__(self):
        self._opts = {}
        self._props = {}
        self._steps = []
        self._step_cnt = 0
        self._perm_cnt = 0

    def add_opt(self, key, obj):
        """Add option (iterable attribute)."""
        self._opts[key] = obj["val"]
        self._steps.append({"key": key, "steps": obj["cnt"]})
        self._step_cnt += 1
        self._perm_cnt += obj["cnt"]

    def add_prop(self, key, obj):
        """Add a property (non-iterable attribute)."""
        self._props[key] = obj["val"]

    def add_opts_from_config(self, opts):
        """Add opt from config."""
        for opt in opts:
            self.add_opt(opt, ConfigLoader.load(opt))

    def get_opt(self, key, default=None):
        """Get opt."""
        if key in self._opts:
            return self._opts[key]
        elif default is not None:
            return default
        else:
            raise Exception(f"Option '{key}' not found")

    def get_prop(self, key, default=None):
        """Get prop."""
        if key in self._props:
            return self._props[key]
        elif default is not None:
            return default
        else:
            raise Exception(f"Property '{key}' not found")

    def get_step_cnt(self):
        """Get total steps."""
        return self._step_cnt

    def get_perm_cnt(self):
        return self._perm_cnt


class SpriteGenerator:
    """Generate sprite of training data."""

    def __init__(self):
        """Init."""
        # opts = GeneratorOptions()
        # opts.add_opts_from_config(["words", "fonts", "blurs",
        #                            "rotations", "backgrounds"])
        #
        # sprite_dims = find_best_sprite_dims(opts.get_perm_cnt())
        #
        # img_props = {"width": config.SPRITE_WIDTH * sprite_dims[0],
        #              "height": config.SPRITE_HEIGHT * sprite_dims[1],
        #              "sprite_width": config.SPRITE_WIDTH,
        #              "sprite_height": config.SPRITE_HEIGHT,
        #              "dpi": config.SPRITE_DPI,
        #              "colorspace": config.SPRITE_COLORSPACE}
        # text_props = {"x_offset": config.TEXT_X_OFFSET,
        #               "y_offset": config.TEXT_Y_OFFSET}
        #
        # opts.add_prop("img_props", img_props)
        # opts.add_prop("text_props", text_props)
        #
        # logging.info(f"total perms: {self._opts.get_perm_cnt()}")
        # logging.info(f"total steps: {self._opts.get_step_cnt()}")
        pass

    def get_dir(self, word):
        """Gets dir (and makes sure it exists.)"""
        path = f"{config.TRAINING_DATA_PATH}/{word[0]}/{word}"
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def name_image(self, word, font, blur, rot):
        """Get programmatic name for generated image."""
        return f"{self.get_dir(word)}/{word}-b{blur}-r{rot}.png"

    def generate(self):
        """Generate. @TODO migrate to opts in config."""
        blurs = config.BLURS
        fonts = config.FONTS

        blur_min = config.BLUR_RADIUS_MIN
        blur_max = config.BLUR_RADIUS_MAX
        blur_incr = config.BLUR_RADIUS_INCREMENT
        blur_steps = int((blur_max - blur_min) / blur_incr)

        rot_min = config.ROTATION_MIN
        rot_max = config.ROTATION_MAX
        rot_incr = config.ROTATION_INCREMENT
        rot_steps = int((rot_max - rot_min) / rot_incr)

        wl = []
        with open(config.WORD_LIST) as fh:
            for row in fh:
                wl.append(row.strip())

        for word in wl:
            logging.info(f"{word}")
            for font in fonts:
                pil_font = ImageFont.truetype(
                    font=font, size=config.FONT_SIZES[0])

                (img_w, img_h) = pil_font.getsize(word)

                # blur types
                for blur in blurs:
                    # blur amounts
                    for blur_step in range(0, blur_steps):
                        cur_blur = blur_min + blur_step * blur_incr
                        # rotations
                        for rot_step in range(0, rot_steps):
                            cur_rot = rot_min + rot_step * rot_incr
                            self.draw(word, font, blur, cur_blur, cur_rot,
                                      pil_font)

    def draw(self, word, font, blur, cur_blur, cur_rot, pil_font):
        """Draw on image."""
        start_x = config.TEXT_X_OFFSET
        start_y = (config.SPRITE_HEIGHT - config.TEXT_Y_OFFSET
                   * 2 - config.FONT_SIZES[0]) / 2
        img_name = self.name_image(word, font, cur_blur, cur_rot)
        img = Image.new(config.SPRITE_COLORSPACE,
                        (config.SPRITE_WIDTH, config.SPRITE_HEIGHT),
                        color=config.SPRITE_BGS[0])

        # add text
        draw = ImageDraw.Draw(img)
        draw.text((start_x, start_y), word, font=pil_font)

        # add blur
        im1 = None
        if blur == "BoxBlur":
            im1 = img.filter(ImageFilter.BoxBlur(cur_blur))
            img = im1
        elif blur == "GaussianBlur":
            im1 = img.filter(ImageFilter.BoxBlur(cur_blur))
            img = im1

        # add rotation
        im1 = img.rotate(cur_rot, fillcolor=config.SPRITE_BGS[0])
        img = im1

        img.save(f"{img_name}", "PNG")
