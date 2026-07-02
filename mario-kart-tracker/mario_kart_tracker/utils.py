from django.db import transaction
from .models import *

import re

'''
Takes a game version and returns the associated session options (the 'context').

Returns the available characters, vehicles, wheels, and gliders

If no game version is provided, returns an error
'''
def get_game_context(game: GameVersion):
    if not game:
        raise TypeError("get_game_context() requires a game model object")
    
    characters = Character.objects.filter(game_version=game)
    vehicles = Vehicle.objects.filter(game_version=game)
    gliders = Glider.objects.filter(game_version=game)
    wheels = Wheel.objects.filter(game_version=game)
    game_context = {
        "characters": characters,
        "vehicles": vehicles,
        "gliders": gliders,
        "wheels": wheels,
        "game_version_id": game.game_version_id
    }

    return game_context

@transaction.atomic
def save_race_results(request):
    # Get the session
    session = Session.objects.get(pk=request.POST.get("session"))

    # Get the race no.
    race_no = int(request.POST.get("race-no"))

    # Get the track(s)
    start_track = Track.objects.filter(
        game_version = session.game_version,
        name = request.POST.get("start-track")
    ).first()
    end_track = Track.objects.filter(
        game_version = session.game_version,
        name = request.POST.get("end-track")
    ).first()

    # Save the race
    race, created = Race.objects.update_or_create(
        session = session, race_no = race_no,
        defaults={
            "start_track": start_track,
            "end_track": end_track
        }
    )

    # For each player, get their position
    for form_item in list(request.POST.items()):
        if re.match(r"player-\d+-position", form_item[0]):
            player_id = re.search(r"\d+", form_item[0]).group()
            player = PlayerSession.objects.filter(session = session, player_id = player_id).first()

            result = Position.objects.filter(
                game_version = session.game_version,
                position = int(form_item[1])
            ).first()
            if not result:
                ValueError("No position found")
            
            # Save the player results
            race_result = RaceResult.objects.update_or_create(
                race = race, player_session = player,
                defaults={"position": result}
            )

            print(race_result)

    # Everything worked fine, so return
    return True