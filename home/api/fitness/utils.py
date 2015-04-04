# -*- coding: utf-8 -*-
import random
from collections import namedtuple

from .fto import (get_ceiling, get_max_from_previous, calc_warmup_sets,
                  weeks, lbs2kg)
from .models import Exercise

__author__ = 'Jon Nappi'


def crank(apex=100, set_max=10, start=1):
    """Generator for set/rep schemes. Calculates progressing reps and sets of
    an exercise. Progresses in a pyramid-style scheme, where reps and sets are
    initially added, and then consolidated once an arbitrary critical number
    of total reps have been reached.

    :param int apex: Top number of reps to perform *in toto*
    :param int set_max: Top number of reps to perform per set
    :param int start: Reps to start at. Numbers greater than `apex` indicate
        we're in the aggregative phase, and are consolidating reps into fewer
        sets.
    """
    def divvy():
        # Divvy up our reps into sets
        divvy_sets = [set_max] * (start // set_max)
        mod = start % set_max
        if mod:
            divvy_sets.append(mod)
        return divvy_sets

    sets = divvy()
    curr = start
    # Continue to crank until it's only one set
    while sets[0] < apex:
        # Yield a sequence of reps
        yield sets

        # Crank
        if sum(sets) < apex:
            # Accumulate
            pass
        curr += 1

    assert len(sets) == 1, 'Should terminate with one set left'


def build_sets(prev_weight, curr_week, unit='lbs', increment=0):
    """Create sets based off last week's top weight.

    :param int max_weight: Training max weight.
    :param float top_percent: Percentage of our one rep max the top working
        set will be calculated at.
    :param str unit: Whether to calculate in lbs or kgs
    """
    ceiling_func = get_ceiling(unit)
    max_weight = get_max_from_previous(prev_weight, curr_week)
    # Bump weight if this is the start of a new cycle
    max_weight += increment if curr_week == 1 else 0
    # Create warm-up sets
    sets = calc_warmup_sets(max_weight, unit)

    # We work our way up to the top percent
    for i in (2, 1, 0):
        # Subtract 10% to only use a 90% training max
        training_percent = weeks[curr_week].percent - 0.1 * i
        weight = ceiling_func(training_percent * max_weight)
        sets.append(weight)
    if unit is 'kg':
        sets = lbs2kg(sets)
    return sets


def select_exercises(group):
    """Given a specified muscle *group*, generate a pseudo-random set of
    exercises targeting that muscle group

    :param group: One of the muscle groups specified in
        fitness.models.MUSCLE_GROUPS
    """
    filter_args = dict(primary_muscle_group=group)
    excs = list(Exercise.objects.filter(**filter_args).order_by('-last_done'))

    selected = []
    for index in range(10):
        try:
            exercise = excs.pop(random.randint(0, len(excs)))
            if exercise.last_weight is None and exercise.last_reps is None:
                pass
            elif exercise.last_weight is None:
                increase = exercise.last_reps * exercise.progress_differential
                exercise.last_reps += increase
                exercise.save()
            elif exercise.last_reps is None:
                increase = exercise.last_weight * exercise.progress_differential
                exercise.last_weight += increase
                exercise.save()
            selected.append(exercise)
        except IndexError:  # We didn't have enough exercises in this group
            pass
    return selected


Set = namedtuple('Set', ['name', 'weights'])


def generate_sets(exercises):
    """For each exercise in *exercises*, generate sets of weights for that
    exercise

    :param exercises: A list of fitness.models.Exercise's
    """
    return [Set(exercise.name, build_sets(exercise.last_weight, 1))
            for exercise in exercises]
