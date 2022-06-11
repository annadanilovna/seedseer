"""Loads config values."""

from . import config
from .util import calc_steps, has_method


class ConfigLoader:
    """Config loading."""

    @staticmethod
    def load(k):
        """Load param set from config."""
        func = has_method(ConfigLoader, f"_load_{k}")
        if func:
            return func()
        else:
            return ConfigLoader._load_blank()

    @staticmethod
    def payload(val, cnt):
        return {"val": val, "cnt": cnt}

    @staticmethod
    def _load_blank():
        """Load blank config like opts list and zero."""
        return ConfigLoader.payload([], 0)

    @staticmethod
    def _load_words():
        """Load words from config."""
        words = []
        with open(config.WORD_LIST) as fh:
            words = [row.strip() for row in fh]
        return ConfigLoader.payload(words, len(words))

    @staticmethod
    def _load_blurs():
        """Load blurs from config."""
        opts = []
        b_max = config.BLUR_RADIUS_MAX
        b_min = config.BLUR_RADIUS_MIN
        b_incr = config.BLUR_RADIUS_INCREMENT
        b_steps = calc_steps(b_min, b_max, b_incr)

        for blur in config.BLURS:
            opts.append({"func": blur,
                         "b_min": b_min,
                         "b_max": b_max,
                         "b_incr": b_incr,
                         "b_steps": b_steps})

        return ConfigLoader.payload(opts, len(opts) * b_steps)

    @staticmethod
    def _load_rotations():
        """Load rotations from config."""
        r_min = config.ROTATION_MIN
        r_max = config.ROTATION_MAX
        r_incr = config.ROTATION_INCREMENT
        r_steps = calc_steps(r_min, r_max, r_incr)
        return ConfigLoader.payload([{"r_min": r_min,
                                      "r_max": r_max,
                                      "r_incr": r_incr}],
                                    r_steps)

    @staticmethod
    def _load_fonts():
        """Load fonts from config."""
        fonts = config.FONTS
        sizes = config.FONT_SIZES
        colors = config.FONT_COLORS

        opts = []
        for font in fonts:
            for size in sizes:
                for color in colors:
                    opts.append({"font": font, "color": color, "size": size})
        return ConfigLoader.payload(opts,
                                    len(opts) * len(sizes) * len(colors))

    @staticmethod
    def _load_backgrounds():
        """Load backgrounds from config."""
        return ConfigLoader.payload(config.SPRITE_BGS,
                                    len(config.SPRITE_BGS))
