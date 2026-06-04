from django.urls import path

from . import views

app_name = "mk-tracker"
urlpatterns = [
    path("", views.index, name="index"),
    path("players/", views.player_list, name="player-list"),
    path("player/", views.edit_player, name="new-player"),
    path("player/<int:player_id>/", views.edit_player, name="player-setup"),
    path("player/save_player", views.save_player, name='save-player'),
    path("save-player-default/", views.save_player_default, name='save-player-default'),
    path("session/", views.session_setup, name="new-session"),
    path("save-session", views.start_new_session, name="save-session"),
    path("session/<int:session_id>/", views.session_setup, name="session-setup"),
    path("session/<int:session_id>/<int:race_no>", views.race_entry, name="race-entry")
]