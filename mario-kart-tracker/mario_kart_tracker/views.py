from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
from .utils import *

# Create your views here.
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
    )
    # BUT! we need to verify that only one is returned - just in case
    if len(selected_character) > 1:
        raise ValueError("Only one selection is allowed")
    else:
        selected_character = selected_character.first()

    selected_vehicle = Vehicle.objects.filter(
        game_version=game_version,
        name=request.POST.get("default-vehicle")
    )
    if len(selected_vehicle) > 1:
        raise ValueError("Only one selection is allowed")
    else:
        selected_vehicle = selected_vehicle.first()
    
    selected_wheel = Wheel.objects.filter(
        game_version=game_version,
        name=request.POST.get("default-wheel")
    )
    if len(selected_wheel) > 1:
        raise ValueError("Only one selection is allowed")
    else:
        selected_wheel = selected_wheel.first()
    
    selected_glider = Glider.objects.filter(
        game_version=game_version,
        name=request.POST.get("default-glider")
    )
    if len(selected_glider) > 1:
        raise ValueError("Only one selection is allowed")
    else:
        selected_glider = selected_glider.first()

    print(type(selected_character))

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
    return HttpResponse()


def get_player_defaults(request):
    player_id = request.GET.get('player')
    game_version_id = request.GET.get('game')

    defaults = PlayerDefault.objects.filter(
        player_id = player_id,
        game_version_id = game_version_id
    )

    return defaults


def race_entry(request, session_id, race_no):
    response = f'''
<h1>Enter Race Results</h1>
<p>Session: {session_id}, Race No.: {race_no}
'''
    return HttpResponse(response)