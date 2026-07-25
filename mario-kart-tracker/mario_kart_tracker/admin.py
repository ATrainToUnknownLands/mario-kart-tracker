from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(GameVersion)
class GameVersionAdmin(admin.ModelAdmin):
    pass

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "game_version")


@admin.register(CourseSelection)
class CourseSelectionAdmin(admin.ModelAdmin):
    list_display = ("name", "game_version")


@admin.register(CpuDifficulty)
class CpuDifficultyAdmin(admin.ModelAdmin):
    list_display = ("name", "game_version")


@admin.register(EngineClass)
class EngineClassAdmin(admin.ModelAdmin):
    list_display = ("name", "game_version")


@admin.register(VehicleOption)
class VehicleOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "game_version")


@admin.register(Glider)
class GliderAdmin(admin.ModelAdmin):
    pass


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    pass


@admin.register(Wheel)
class WheelAdmin(admin.ModelAdmin):
    pass


@admin.register(ItemRule)
class ItemRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "game_version")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("position", "game_version")


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("name", "game_version")


@admin.register(PlayerDefault)
class PlayerDefaultAdmin(admin.ModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass


@admin.register(PlayerSession)
class PlayerSessionAdmin(admin.ModelAdmin):
    pass


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    pass


@admin.register(RaceResult)
class RaceResultAdmin(admin.ModelAdmin):
    pass

