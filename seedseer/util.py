"""Various utility functions."""

import math
import os
import pathlib

from . import config


def check_paths_exist():
    """Checks if path exists and if not, makes it."""
    for path in config.CHECK_PATHS:
        if not os.path.isdir(path):
            os.path.makedirs(path)
    return True


def has_method(cls, func):
    """Return True if class has a method else False."""
    try:
        f = hasattr(cls, func)
        if callable(f):
            return f
    except:
        pass
    return None


def calc_steps(min, max, incr):
    """Given min, max, and incr calculate the number of steps in the cycle."""
    return 1 + (max - min) / incr


def get_factors(n):
    """Get factors of a number."""
    n = int(n)
    f = [1, n]
    i = 2

    if n % 2 == 0:
        i = 3
        f += [2, int(n / 2)]

    incr = i - 1
    itr = 0
    j = int(n / (i + 1))

    while i < j + 1:
        d = n / i
        if int(d) == d:
            f += [i, int(d)]
        i += incr
        j = int(n / (i + 1)) + 1
        itr += 1
    return list(dict.fromkeys(f))


def find_best_sprite_dims(n):
    """Find best dimensions for spritesheet."""
    # closest = math.ceil(math.sqrt(n))
    # rem = n % closest
    #
    # if rem == 0:
    #     return [closest, closest]
    # else:
    #     full_fit = None
    #     full_fit_best = 1
    #     f = sorted(get_factors(n))
    #     for i in f:
    #         j = int(n / i)
    #         d = math.abs(1 - i / j)
    #         if d > full_fit_best:
    #             full_fit = [i, j]
    #             full_fit_best = d
    # if full_fit_best < 0.1:
    #     return full_fit
    # else:
    #     return closest
    c1 = math.ceil(math.sqrt(n))
    c2 = math.ceil(n / c1)
    return [c1, c2]
