from .models import *

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