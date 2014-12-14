# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View

from home.api.fitness.utils import select_exercises, generate_sets

from .forms import WorkoutForm

__author__ = 'Jon Nappi'


class WorkoutView(View):
    def get(self, request):
        return render(request, 'workout.html', {'form': WorkoutForm})

    def post(self, request):
        exercises = select_exercises(request.POST.get('muscle_group'))
        sets = generate_sets(exercises)

        context = {'sets': sets, 'form': WorkoutForm}
        return render(request, 'workout.html', context)
