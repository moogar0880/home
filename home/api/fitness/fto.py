# -*- coding: utf-8 -*-
import math
from math import ceil as fine_ceil
from collections import namedtuple

__author__ = 'Jon Nappi'

Week = namedtuple('Week', ['percent', 'reps'])


def map_weeks():
    """Map training week to prescribed percent and repetitions."""
    reps_by_week = (
        (5, 5, 10),
        (3, 3, 8),
        (5, 3, 5)
    )
    percents_by_week = (0.85, 0.90, 0.95)

    return [None] + list(map(Week, percents_by_week, reps_by_week))

# First index is empty to allow for direct indexing by week number
_weeks = map_weeks()


def coarse_ceil(f):
    """Find ceiling of number, a la 5/3/1 method."""
    # Apply modulus to weight in increments of 5
    mod = math.fmod(f, 5)
    # Short heuristic to determine rounding
    if mod > 2.5:  # round up
        return math.trunc(f - mod + 5)
    else:  # round down
        return math.trunc(f - mod)


def lbs2kg(sets, sub=0):
    """Convert a set of weights in pounds to kilograms.

    :param list sets: Iterable of prescribed weights.
    :param int sub: Amount to subtract from each converted weight. Useful
    for when taking into account bar weight.
    """
    lb_kg = lambda w: int(round(w / 2.20462) - sub)
    return (lb_kg(x) for x in sets)


def one_rep(weight, week=1, inc=5):
    """Calculate one rep max from week's percentage."""
    percents = (0.85, 0.9, 0.95)
    percent = percents[week]
    return weight / percent + inc if week == 3 else 0


def zip_sets(weights, week=1):
    """Attach repeptitions to given weights."""
    warm_up_reps = (5, 5, 3)
    reps = warm_up_reps + _weeks[week-1]
    sets = zip(weights, reps)
    output = ''
    for s in sets:
        output += ' {} x {},'.format(s[0], s[1])
    return output.rstrip(', ')

weeks = map_weeks()


def get_ceiling(unit='lbs'):
    """Return correct ceiling function by units.

    Python's `ceil` function rounds to the nearest integer, while 5/3/1 calls
    for rounding to the nearest multiple of five. We use the finer-grained
    :func:`ceil` when in kilograms, since jumps of 1 kg are possible.
    """
    return coarse_ceil if unit == 'lbs' else fine_ceil


def get_max_from_previous(prev_weight, curr_week):
    """Calculate this mesocycle's top weight by using last week's weight."""
    # Get our maximum weight for this mesocycle (~month)
    # Do so by dividing last week's weight by last week's percentage
    last_week = curr_week - 1
    # Feeling dumb, so I can't get this modulo to work out right.
    # 3 => 2
    # 2 => 1
    # 1 => 3 (Skips zero)
    if prev_weight is None:
        prev_weight = 0
    prev_week = last_week if last_week != 0 else len(weeks) - 1
    max_weight = prev_weight / weeks[prev_week].percent
    return max_weight


def calc_warmup_sets(max_weight, unit='lbs'):
    """Return warm-up sets, based on top weight of the day."""
    percents = (0.4, 0.5, 0.6)
    ceiling_func = get_ceiling(unit)
    calc_warmups = lambda percent: ceiling_func(max_weight * percent)
    return list(map(calc_warmups, percents))