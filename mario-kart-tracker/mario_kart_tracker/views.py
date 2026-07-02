from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.db import transaction
from django.urls import reverse

from .models import *
from .utils import *

import re

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

    return HttpResponseRedirect(f"./session/{new_session.session_id}/1")

from django.db.models import Max

def race_entry(request, session_id, race_no):
    print(f"session_id: {session_id}, race_no: {race_no}")

    # Get the tracks for the game being played
    session = Session.objects.get(pk=session_id)
    tracks = Track.objects.filter(game_version=session.game_version)

    # Get existing race results
    existing_race = Race.objects.filter(session=session, race_no=race_no).first()

    # Get the players
    players = []
    player_sessions = PlayerSession.objects.filter(session=session)
    for player_session in player_sessions:
        player_context = {}
        player_context["player_session"] = player_session
        # If the race has already been entered (the user is returning to the page),
        # Get the positions of the players (if they exist)
        if existing_race:
            race_result = RaceResult.objects.filter(race=existing_race, player_session=player_session).first()
            if race_result:
                player_context["result"] = race_result
        players.append(player_context)

    # Get the positions
    positions = Position.objects.filter(game_version=session.game_version)

    # Get the last place position in the game (for form validation)
    max_position = positions.aggregate(Max("position"))

    # Assemble the context
    context = {
        "race_no": race_no,
        "session": session,
        "tracks": tracks,
        "players": players,
        "positions": positions,
        "max_position": max_position["position__max"],
        "result_tracks": existing_race
    }

    # Return the rendered page
    return render(request, "mario_kart_tracker/race-entry.html", context)


'''
Save the results of a particular race.
Saves the track(s) on which the race occurred, and the results for each player
'''
def next_race(request):
    saved = save_race_results(request)
    if not saved:
        raise Exception("Something went wrong!")

    # Get the session
    session = Session.objects.get(pk=request.POST.get("session"))

    # Get the race no.
    race_no = int(request.POST.get("race-no"))

    # If there are any more races to go
    if race_no < session.no_races:
        # Continue to the next race
        return HttpResponseRedirect(reverse("mk-tracker:race-entry", kwargs={
            "session_id": session.session_id,
            "race_no": race_no + 1
        }))
    else:
        # Otherwise, mark the session as finished
        session.is_complete = True
        session.save()

        # Then send the user to the finished screen
        return HttpResponse("Session completed. Thanks for playing!")


def previous_race(request):
    if request.POST.get("start-track"):
        saved = save_race_results(request)
        if not saved:
            raise Exception("Something went wrong!")
    else:
        print("Nothing to save")

    # Get the session
    session = Session.objects.get(pk=request.POST.get("session"))

    # Get the race no.
    race_no = int(request.POST.get("race-no"))

    # The user wants to go back, so redirect to the previous race
    return HttpResponseRedirect(reverse("mk-tracker:race-entry", kwargs={
            "session_id": session.session_id,
            "race_no": race_no - 1
        }))


def get_player_defaults(request):
    # Get the player and game version
    player_id = request.GET.get('player_id')
    game_version_name = request.GET.get('game_version')
    game_version = GameVersion.objects.filter(short_name = game_version_name).first()

    # Get the defaults model object
    defaults_raw = PlayerDefault.objects.filter(
        player_id = player_id,
        game_version = game_version
    ).first()

    if defaults_raw:
        # Return only the relevant fields
        fields = ["character", "vehicle", "wheel", "glider"]
        defaults = {}
        # We want the text representation (the name), not the id, so we need to 
        # get the "name" field for each model
        for field in fields:
            attr = getattr(defaults_raw, field, False)
            if attr:
                defaults[field] = attr.name
            else:
                defaults[field] = attr
    else:
        # If there aren't any defaults, just return nothing
        print("No defaults")
        raise Http404("No defaults for this game for this player")
    
    return JsonResponse(defaults, safe=False)