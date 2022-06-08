"""Generate training images."""

import os

from PIL import ImageFont, ImageDraw, Image, ImageFilter

from . import config


def get_dir(word):
    """Gets dir (and makes sure it exists.)"""
    path = f"{config.TRAINING_DATA_PATH}/{word[0]}/{word}"
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def name_image(word, font, blur, rot):
    """Get programmatic name for generated image."""
    return f"{get_dir(word)}/{word}-b{blur}-r{rot}.png"


def generate():

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
        for font in fonts:
            pil_font = ImageFont.truetype(font=font, size=14)
            (img_w, img_h) = pil_font.getsize(word)
            img_w = int(img_w * 1.2)
            img_h = int(img_h * 1.2)
            start_x = int(img_w * 0.1)
            start_y = int(img_h * 0.1)

            # blur types
            for blur in blurs:

                # blur amounts
                for blur_step in range(0, blur_steps):
                    cur_blur = blur_min + blur_step * blur_incr

                    # rotations
                    for rot_step in range(0, rot_steps):
                        cur_rot = rot_min + rot_step * rot_incr
                        # img = rotate_image(img, cur_rot)
                        im1 = None
                        img_name = name_image(word, font, cur_blur, cur_rot)
                        img = Image.new("L", (img_w, img_h), color="white")
                        draw = ImageDraw.Draw(img)
                        draw.text((start_x, start_y), word, font=pil_font)
                        if blur == "BoxBlur":
                            im1 = img.filter(ImageFilter.BoxBlur(cur_blur))
                            img = im1
                        elif blur == "GaussianBlur":
                            im1 = img.filter(ImageFilter.BoxBlur(cur_blur))
                            img = im1

                        img.save(f"{img_name}", "PNG")