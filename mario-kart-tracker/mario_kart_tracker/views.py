from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.db import transaction
from django.forms.models import model_to_dict

from .models import *
from .utils import *

import re

# TODO: implement form verification

def index(request):
    return HttpResponse("Hello World. This is the Mario Kart Tracker index!")


def player_list(request):
    players = Player.objects.all()
    context = {"player_list": players}

    return render(request, "mario_kart_tracker/player-list.html", context)


def edit_player(request, player_id=None):
    context = {}

    if player_id:
        player = Player.objects.get(pk=player_id)
        context["player"] = player

        player_defaults = PlayerDefault.objects.filter(player=player)

        # Sort the default sets into different keys for the context
        for default_set in player_defaults:
            defaults_for_game = default_set.game_version.short_name
            context[f'defaults_{defaults_for_game}'] = default_set

    for game in GameVersion.objects.all():
        key_name = game.short_name
        context[key_name] = get_game_context(game)
    
    return render(request, "mario_kart_tracker/player-setup.html", context)


def save_player(request):
    new_player = Player(name=request.POST.get("player-name"))
    new_player.save()

    new_id = new_player.player_id

    return HttpResponseRedirect(f'../player/{new_id}')


def save_player_default(request):
    player = Player.objects.get(pk=request.POST.get("default-player"))
    game_version = GameVersion.objects.get(pk=request.POST.get("default-game"))

    # We have to get the details by name - since name is unique to the game, this
    # is trivial
    selected_character = Character.objects.filter(
        game_version=game_version,
        name=request.POST.get("default-character")
    ).first()

    selected_vehicle = Vehicle.objects.filter(
        game_version=game_version,
        name=request.POST.get("default-vehicle")
    ).first()
    
    selected_wheel = Wheel.objects.filter(
        game_version=game_version,
        name=request.POST.get("default-wheel")
    ).first()
    
    selected_glider = Glider.objects.filter(
        game_version=game_version,
        name=request.POST.get("default-glider")
    ).first()

    defaults, created = PlayerDefault.objects.update_or_create(
        game_version=game_version, player=player,
        defaults={
            "character": selected_character,
            "vehicle": selected_vehicle,
            "wheel": selected_wheel,
            "glider": selected_glider
        }
    )

    return HttpResponse(f"Defaults saved!")


def session_setup(request):
    context = {}

    for game in GameVersion.objects.all():
        key_name = game.short_name
        context[key_name] = get_game_context(game)

        # Get the Course Selection Mode, Item Rules, Engine Classes, and Difficulties
        context[key_name]["track_modes"] = CourseSelection.objects.filter(game_version=game)
        context[key_name]["item_rules"] = ItemRule.objects.filter(game_version=game)
        context[key_name]["engine_classes"] = EngineClass.objects.filter(game_version=game)
        context[key_name]["cpu_difficulties"] = CpuDifficulty.objects.filter(game_version=game)

    players = Player.objects.all()

    context["players"] = players

    return render(request, "mario_kart_tracker/session-setup.html", context)


'''
Start a new VS Session. Get all the details and save to the database
'''
@transaction.atomic
def start_new_session(request):
    # Get the form responses
    game            = GameVersion.objects.get(pk=request.POST.get("game_version"))
    no_players      = request.POST.get("no-players")
    track_choice    = CourseSelection.objects.get(pk=request.POST.get("track-choice"))
    engine_class    = EngineClass.objects.get(pk=request.POST.get("cc"))
    item_rule       = ItemRule.objects.get(pk=request.POST.get("item-rule"))
    com_difficulty  = CpuDifficulty.objects.get(pk=request.POST.get("difficulty"))
    no_races        = request.POST.get("no-races")
    no_teams        = request.POST.get("no-teams")

    new_session = Session(
        no_players = no_players,
        game_version = game,
        no_races = no_races,
        engine_class = engine_class,
        teams = no_teams,
        item_rule = item_rule,
        cpu_difficulty = com_difficulty,
        course_selection = track_choice
    )

    new_session.save()
    player_session_ids = []

    for player_no in range(1, int(no_players) + 1):
        player = Player.objects.get(pk=request.POST.get(f"player-select{player_no}"))
        selected_character = Character.objects.filter(
            game_version=game,
            name=request.POST.get(f"player{player_no}-character")
        ).first()

        selected_vehicle = Vehicle.objects.filter(
            game_version=game,
            name=request.POST.get(f"player{player_no}-vehicle")
        ).first()
        
        selected_wheel = Wheel.objects.filter(
            game_version=game,
            name=request.POST.get(f"player{player_no}-wheel")
        ).first()
        
        selected_glider = Glider.objects.filter(
            game_version=game,
            name=request.POST.get(f"player{player_no}-glider")
        ).first()

        
        player_session = PlayerSession(
            session = new_session,
            player = player,
            character = selected_character,
            vehicle = selected_vehicle,
            wheel = selected_wheel,
            glider = selected_glider
        )

        player_session.save()

        player_session_ids.append(player_session.player_session_id)

    return HttpResponseRedirect(f"../session/{new_session.session_id}/1")


def race_entry(request, session_id, race_no):
    print(f"session_id: {session_id}, race_no: {race_no}")

    # Get the tracks for the game being played
    session = Session.objects.get(pk=session_id)
    tracks = Track.objects.filter(game_version=session.game_version)

    # Get the players
    players = PlayerSession.objects.filter(session=session)
    players = [player_session.player for player_session in players]

    # Get the positions
    positions = Position.objects.filter(game_version=session.game_version)

    # Assemble the context
    context = {
        "race_no": race_no,
        "session": session,
        "tracks": tracks,
        "players": players,
        "positions": positions
    }

    # Return the rendered page
    return render(request, "mario_kart_tracker/race-entry.html", context)


'''
Save the results of a particular race.
Saves the track(s) on which the race occurred, and the results for each player
'''
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
    race = Race(
        session = session,
        race_no = race_no,
        start_track = start_track,
        end_track = end_track
    )
    race.save()

    # For each player, get their position
    for form_item in list(request.POST.items()):
        if re.match(r"player-\d+-position", form_item[0]):
            player_id = re.search(r"\d+", form_item[0]).group()
            player = Player.objects.get(pk=int(player_id))
            result = Position.objects.filter(
                game_version = session.game_version,
                position = int(form_item[1])
            ).first()
            if not result:
                ValueError("No position found")
            
            # Save the player results
            race_result = RaceResult(
                race = race,
                player = player,
                position = result
            )

            race_result.save()

    # If there are any more races to go
    if race_no < session.no_races:
        # Continue to the next race
        return HttpResponseRedirect(f"../session/{session.session_id}/{race_no + 1}")
    else:
        # Otherwise, mark the session as finished
        session.is_complete = True
        session.save()

        # Then send the user to the finished screen
        return HttpResponse("Session completed. Thanks for playing!")
    


def get_player_defaults(request):
    player_id = request.GET.get('player_id')
    game_version_name = request.GET.get('game_version')

    game_version = GameVersion.objects.filter(short_name = game_version_name).first()

    defaults = PlayerDefault.objects.filter(
        player_id = player_id,
        game_version = game_version
    ).first()

    if defaults:
        defaults = model_to_dict(defaults, fields=["character", "vehicle", "wheel", "glider"])
    else:
        print("No defaults")
        raise Http404("No defaults for this game for this player")
    
    return JsonResponse(defaults, safe=False)