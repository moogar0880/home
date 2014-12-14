# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

from home.fitness.views import WorkoutView

__author__ = 'Jon Nappi'

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', WorkoutView.as_view(), name='home'),
    url(r'^fitness/', WorkoutView.as_view(), name='fitness'),
)
