from django.conf.urls import patterns, url

from .views import WorkoutView

urlpatterns = patterns(
    '',
    url(r'^fitness/', WorkoutView.as_view(), name='fitness'),
)
