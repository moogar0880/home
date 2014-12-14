# -*- coding: utf-8 -*-
from django import forms

from home.api.fitness.models import MUSCLE_GROUPS

__author__ = 'Jon Nappi'


class WorkoutForm(forms.Form):
    muscle_group = forms.ChoiceField(choices=MUSCLE_GROUPS)
