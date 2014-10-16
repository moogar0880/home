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

    # Record keeping for the last go at this exercise
    last_done = models.DateTimeField(null=True, blank=True)
    last_weight = models.FloatField(null=True, blank=True)
    last_reps = models.IntegerField(null=True, blank=True)

    # The rate at which weight/reps for this excercise should be increased by
    progress_differential = models.IntegerField(null=True, blank=True)

    # Categorization fields
    primary_muscle_group = models.CharField(max_length=2, choices=MUSCLE_GROUPS)
    secondary_muscle_group = models.CharField(max_length=2, null=True,
                                              blank=True, choices=MUSCLE_GROUPS)
    category = models.CharField(max_length=1, choices=EXCERCISE_CATEGORIES)

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
