from itertools import tee
from django.db import models


EXCERCISE_CATEGORIES = (('R', 'Resistance'),
                        ('F', 'Functional'),
                        ('C', 'Cardio'))

MUSCLE_GROUPS = (('CH', 'Chest'),
                 ('L', 'Legs'),
                 ('T', 'Triceps'),
                 ('BA', 'Back'),
                 ('BI', 'Biceps'),
                 ('CO', 'Core'),
                 ('S', 'Shoulders'))


class Exercise(models.Model):
    """A Base model type for storing data about a particular exercies"""
    name = models.CharField(max_length=120)
    user_id = models.IntegerField(null=True, blank=True)

    # Record keeping for the last go at this exercise
    last_done = models.DateTimeField(null=True, blank=True)
    last_weight = models.FloatField(null=True, blank=True)
    last_reps = models.IntegerField(null=True, blank=True)

    # The rate at which weight/reps for this excercise should be increased by
    progress_differential = models.FloatField(null=True, blank=True)

    # Categorization fields
    primary_muscle_group = models.CharField(max_length=2, choices=MUSCLE_GROUPS)
    secondary_muscle_group = models.CharField(max_length=2, null=True,
                                              blank=True, choices=MUSCLE_GROUPS)
    category = models.CharField(max_length=1, choices=EXCERCISE_CATEGORIES)

    @staticmethod
    def _drop_index(l):
        """Returns index of the first index in the list less than its
        predecessor"""

        def pairwise(iterable):
            """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
            a, b = tee(iterable)
            next(b, None)
            return zip(a, b)

        # Build
        try:
            # Find the index of the first decrement in the list
            idx = next((i + 1 for i, (a, b) in
                        enumerate(pairwise(l)) if b < a))
        except StopIteration:
            return 0
        # [6, 6, 6, 2] is always going to return 3, so we need to reset to
        # the first element
        # if we're at the end of the list, return the start
        if idx == len(l) - 1:
            return 0
        else:
            return idx

    def _crank(self, sets, s_limit=0):
        if s_limit:     # building
            if (sets[-1] + 1) > s_limit:
                sets.append(1)
            else:
                sets[-1] += 1
        else:           # aggregation
            sets[self._drop_index(sets)] += 1    # add to needy set
            if sets[-1] == 1:   # if last value is 1
                sets.pop()      # remove from list
            else:
                sets[-1] -= 1

        return sets

    def crank(self):
        if self.reps >= self.rep_limit:     # Aggregation phase
            if len(self.sets) == 1:         # Terminal growth
                return self
            s_limit = 0
        else:                               # Building phase
            s_limit = self.set_limit

        self.sets = self._crank(self.sets, s_limit)
        self.reps += 1
        return self

    def divvy_reps(self):
        # Fill AMAP sets up to our set limit
        sets = [self.set_limit for _ in range(self.reps // self.set_limit)]
        # Handle any remaining reps
        spillover = self.reps % self.set_limit
        if spillover:
            sets.append(spillover)

        self.sets = sets
        return self.sets

    def lifetime(self):
        x = Exercise(self.name, 1, self.set_limit, self.rep_limit)
        while x.sets[0] != 2 * x.rep_limit:
            print(x)
            x.crank()

    def __unicode__(self):
        """Output this exercise in the form '<category>: Name'"""
        output = '<{}>: {}'
        cat = None
        for short, long in EXCERCISE_CATEGORIES:
            if self.category == short:
                cat = long
                break
        return output.format(cat, self.name)
    __str__ = __repr__ = __unicode__


class Set:
    def __init__(self, reps=1, set_limit=10, rep_limit=100):
        self.reps = reps
        self.set_limit = set_limit
        self.rep_limit = rep_limit
        self.sets = None


class Workout(models.Model):
    """A Collection of exercises compiled into an individual workout"""
    exercises = models.ManyToManyField('Exercise', blank=True, null=True)

    started = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True, blank=True)

    # The target muscle group for this workout
    focus = models.CharField(max_length=2, choices=MUSCLE_GROUPS)

    def generate_crank(self):
        """'crank' out a list of specific exercises, based on the exercises
        specified for this workout
        """
        return [ex.crank() for ex in Exercise.objects.all() if ex in
                self.exercises.all()]

    def generate(self):
        """Generate a list of exercises for a workout"""
        workouts = []

        return workouts

    def duration(self):
        """Compare the end and start time for the duration of this workout"""
        return self.completed - self.started

    def __unicode__(self):
        """Returns a handy string representation of the current workout"""
        s = ''
        for ex in self.generate():
            s += '{}\n'.format(ex)
        return s
    __str__ = __repr__ = __unicode__
