"""Generate training images."""

import hashlib
import logging
import os
import random
import time

from PIL import ImageFont, ImageDraw, Image, ImageFilter

from . import config
# from .util import has_method, calc_steps, find_best_sprite_dims
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
        random.seed(time.time())
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
        # logging.info(f"total perms: {self._opts.getperm_cnt()}")
        # logging.info(f"total steps: {self._opts.get_step_cnt()}")
        pass

    def get_dir(self, word):
        """Gets dir (and makes sure it exists.)"""
        path = f"{config.TRAINING_DATA_PATH}/{word}"
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def name_image(self, word):
        """Get programmatic name for generated image."""
        h = hashlib.md5(f"{word}{random.random()}".encode("utf-8")).hexdigest()
        return f"{self.get_dir(word)}/{word}-{h[0:10]}.png"

    def init_timing_log(self, predicted_total=None):
        self._tl_st = time.time()
        self._tl_itr = 0
        self._tl_pt = 0
        self._tl_tel = 0
        if predicted_total:
            self._tl_pt = predicted_total

    def update_timing_log(self, force=False):
        self._tl_itr += 1
        if self._tl_itr % config.TL_TIMING_DIV == 0 or force:
            tl_et = time.time()
            el = round(tl_et - self._tl_st, 2)
            self._tl_tel += el
            p = ""
            if self._tl_pt > 0:
                # get % done.
                pct = round((self._tl_itr * 1.0 / self._tl_pt) * 100, 4)
                p = f"{round(pct, 4)}% done"

            logging.info(f"Generated {self._tl_itr} images in {el}s. {p}")
            self._tl_st = tl_et

    def end_timing_log(self):
        self._update_timing_log(force=True)

    def generate(self):
        """Generate. @TODO migrate to opts in config."""

        blurs = config.BLURS
        blur_min = config.BLUR_RADIUS_MIN
        blur_max = config.BLUR_RADIUS_MAX
        blur_incr = config.BLUR_RADIUS_INCREMENT
        blur_steps = int((blur_max - blur_min) / blur_incr)

        rot_min = config.ROTATION_MIN
        rot_max = config.ROTATION_MAX
        rot_incr = config.ROTATION_INCREMENT
        rot_steps = int((rot_max - rot_min) / rot_incr)
        pil_font = ImageFont.truetype(font=config.FONT, size=config.FONT_SIZE)

        bg_steps = len(config.SPRITE_BGS)
        total_steps = blur_steps * rot_steps * bg_steps * 2

        wl_total_steps = total_steps * 1626
        logging.info("Drawing images.")
        logging.info(f"[bs:{blur_steps}, rs:{rot_steps}, tot: {total_steps}]")
        logging.info(f"real total: {wl_total_steps}")

        self.init_timing_log(wl_total_steps)
        with open(config.WORD_LIST) as fh:
            for row in fh:
                word = row.strip()
                # blur types
                for blur in blurs:
                    # blur amounts
                    for blur_step in range(0, blur_steps):
                        cur_blur = blur_min + blur_step * blur_incr
                        # rotations
                        for rot_step in range(0, rot_steps):
                            cur_rot = rot_min + rot_step * rot_incr
                            # background colors
                            for bg_color in config.SPRITE_BGS:
                                self.draw(word, blur, cur_blur,
                                          cur_rot, pil_font,
                                          bg_color)
                                self.update_timing_log()
        self.end_timing_log()

    def draw(self, word, blur, cur_blur, cur_rot, pil_font, bg_color):
        """Draw on image."""
        img_name = self.name_image(word)

        start_x = config.TEXT_X_OFFSET
        start_y = (config.SPRITE_HEIGHT - config.TEXT_Y_OFFSET
                   * 2 - config.FONT_SIZE) / 2

        img = Image.new(config.SPRITE_COLORSPACE,
                        (config.SPRITE_WIDTH,
                         config.SPRITE_HEIGHT),
                        color=bg_color)

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
        im1 = img.rotate(cur_rot, fillcolor=bg_color)
        img = im1

        img.save(f"{img_name}", "PNG")
