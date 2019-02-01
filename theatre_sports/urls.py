from django.urls import path

from .views import match_control, match_scoreboard

urlpatterns = [
    path('match/<match_id>/control', match_control, name='match_control'),
    path('match/<match_id>/scoreboard', match_scoreboard, name='match_scoreboard'),
]
