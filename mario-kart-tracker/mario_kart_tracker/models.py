# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone


class GameVersion(models.Model):
    game_version_id = models.AutoField(primary_key=True, db_comment='Primary key')
    name = models.TextField(unique=True, db_comment="The name of the game, e.g. 'Mario Kart 8 Deluxe'")
    short_name = models.TextField(unique=True, db_comment="Short name of the game, used for coding purposes, eg. 'mk8'")

    class Meta:
        managed = False
        db_table = 'game_version'
        db_table_comment = 'Stores the Mario Kart versions that are available in the app'

    def __str__(self):
        return self.name


class Character(models.Model):
    character_id = models.AutoField(primary_key=True, db_comment='Primary key')
    name = models.TextField(db_comment='The name of the character')
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The game version in which this character appears. Needed for filtering which options are available'
    )

    class Meta:
        managed = False
        db_table = 'character'
        unique_together = (('game_version', 'name'),)
        db_table_comment = 'Stores the characters that may be selected by the player during session setup.'
    
    def __str__(self):
        return self.name


class CourseSelection(models.Model):
    course_selection_id = models.AutoField(primary_key=True, db_comment='Primary key')
    name = models.TextField(db_comment='The name of the course selection regime')
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The game version to which this regime applies. Needed for filtering.'
    )

    class Meta:
        managed = False
        db_table = 'course_selection'
        unique_together = (('name', 'game_version'),)
        db_table_comment = 'Stores the course selection regimes that are available during session setup'
        verbose_name_plural = 'Course Selection Regimes'

    def __str__(self):
        return self.name


class CpuDifficulty(models.Model):
    cpu_difficulty_id = models.AutoField(primary_key=True, db_comment='Primary key')
    name = models.TextField(db_comment='The name of the cpu difficulty level')
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The game version to which this difficulty level applies. Needed for filtering.'
    )

    class Meta:
        managed = False
        db_table = 'cpu_difficulty'
        unique_together = (('name', 'game_version'),)
        db_table_comment = 'Stores the cpu difficulty levels that are available during session setup'
        verbose_name_plural = 'CPU Difficulty Levels'

    def __str__(self):
        return self.name


class EngineClass(models.Model):
    engine_class_id = models.AutoField(primary_key=True, db_comment='Primary key')
    name = models.TextField(db_comment='The name of the engine class (50cc, 100cc, etc.)')
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The game version in which this engine class appears. Needed for filtering which options are available'
    )

    class Meta:
        managed = False
        db_table = 'engine_class'
        unique_together = (('game_version', 'name'),)
        db_table_comment = 'Stores the engine classes that may be selected by the player during session setup.'

    def __str__(self):
        return self.name


class Glider(models.Model):
    glider_id = models.AutoField(primary_key=True, db_comment='Primary key')
    name = models.TextField(unique=True, db_comment='The name of the glider')
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The game version that this glider is in.'
    )

    class Meta:
        managed = False
        db_table = 'glider'
        db_table_comment = 'Stores the names of various glider options that may be selected by the player during session setup\n  \n  This only applies to MK 8, but to allow for future expansion we will include the game version'

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True, db_comment='Primary key')
    name = models.TextField(db_comment='The name of the vehicle')
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The game in which the vehicle appears'
    )

    class Meta:
        managed = False
        db_table = 'vehicle'
        unique_together = (('game_version', 'name'),)
        db_table_comment = 'Stores the names of vehicles that may be selected by the player during session setup.'

    def __str__(self):
        return self.name


class Wheel(models.Model):
    wheel_id = models.AutoField(primary_key=True, db_comment='Primary key')
    name = models.TextField(unique=True, db_comment='The name of the wheels')
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The game version that this wheel is in.'
    )

    class Meta:
        managed = False
        db_table = 'wheel'
        db_table_comment = 'Stores the names of various wheel options that may be selected by the player during session setup.\n  \n  This only applies to MK 8, but to allow for future expansion we will include the game version'

    def __str__(self):
        return self.name


class ItemRule(models.Model):
    item_rule_id = models.AutoField(primary_key=True, db_comment='Primary key')
    name = models.TextField(db_comment='Name of the item rule set')
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The game version to which the rule set applies. Needed for filtering'
    )

    class Meta:
        managed = False
        db_table = 'item_rule'
        unique_together = (('name', 'game_version'),)
        db_table_comment = 'Stores the item rule sets that are available during session setup. May include "custom", but doesn\'t specify which items are included.'

    def __str__(self):
        return self.name


class Player(models.Model):
    player_id = models.AutoField(primary_key=True, db_comment='Primary key')
    name = models.TextField(unique=True, db_comment='Name of the player')

    class Meta:
        managed = False
        db_table = 'player'
        db_table_comment = 'Stores the names of players for whom to store results.'

    def __str__(self):
        return self.name


class Position(models.Model):
    position_id = models.AutoField(primary_key=True, db_comment='Primary key')
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The version of the game to which this result applies'
    )
    position = models.IntegerField(db_comment='The ordinal position')
    points = models.IntegerField(db_comment='The number of points received from this position')

    class Meta:
        managed = False
        db_table = 'position'
        unique_together = (('game_version', 'position'),)
        db_table_comment = 'Stores the scores allocated to each position for each version of the game.'

    def __str__(self):
        return f"{self.position} ({self.points} pts)"


class Track(models.Model):
    track_id = models.AutoField(primary_key=True, db_comment='Primary key')
    name = models.TextField(db_comment='The name of the track')
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The game version containing this track. Used for filtering.'
    )

    class Meta:
        managed = False
        db_table = 'track'
        unique_together = (('name', 'game_version'),)
        db_table_comment = 'Stores the names of tracks to be played during a session.'

    def __str__(self):
        return self.name


class PlayerDefault(models.Model):
    player_default_id = models.AutoField(primary_key=True, db_comment='Primary key')
    player = models.ForeignKey(
        to=Player, 
        on_delete=models.DO_NOTHING, 
        db_comment='The player to whom this default setup applies'
    )
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The game version to which this default setup applies'
    )
    character = models.ForeignKey(
        to=Character, 
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True, 
        db_comment='The character seleted for the default setup'
    )
    vehicle = models.ForeignKey(
        to=Vehicle, 
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True, 
        db_comment='The vehicle selected for the default setup'
    )
    wheel = models.ForeignKey(
        to=Wheel, 
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True, 
        db_comment='The wheels selected for the default setup. MK 8 Deluxe only'
    )
    glider = models.ForeignKey(
        to=Glider, 
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True, 
        db_comment='The glider selected for the default setup. MK 8 Deluxe only'
    )

    class Meta:
        managed = False
        db_table = 'player_default'
        unique_together = (('player', 'game_version'),)
        db_table_comment = 'Favourite setups for a player. A player may have a single favourite setup for each version of Mario Kart. They do not have to make a selection for each option.'


class Session(models.Model):
    session_id = models.AutoField(primary_key=True, db_comment='Primary key')
    no_players = models.IntegerField(db_comment='The number of players that will be in this session')
    game_version = models.ForeignKey(
        to=GameVersion, 
        on_delete=models.DO_NOTHING, 
        db_comment='The Mario Kart version that was played during this session'
    )
    play_date = models.DateTimeField(
        db_comment='The date-time at which the session was played',
        default=timezone.now
    )
    is_complete = models.BooleanField(blank=True, null=True, db_comment='Whether the session was completed. False indicates either that the session is not finished or was finished early. Defaults to `false` then updated on completion')
    no_races = models.IntegerField(db_comment='The number of races that were selected to be played in the session (regardless of how many were actually completed)')
    engine_class = models.ForeignKey(
        to=EngineClass, 
        on_delete=models.DO_NOTHING, 
        db_comment='The engine class selected for the session.'
    )
    teams = models.IntegerField(db_comment='How many teams of racers were selected for this session. 0 indicates no teams.')
    item_rule = models.ForeignKey(
        to=ItemRule, 
        on_delete=models.DO_NOTHING, 
        db_comment='The selected item rules for this session.'
    )
    cpu_difficulty = models.ForeignKey(
        to=CpuDifficulty, 
        on_delete=models.DO_NOTHING, 
        db_comment='The CPU difficulty level selected for this session.'
    )
    vehicle_selection = models.TextField(blank=True, null=True, db_comment='The types of vehicles that may be used by the CPU for this session. Applies to MK 8 Deluxe only.')
    course_selection = models.ForeignKey(
        to=CourseSelection, 
        on_delete=models.DO_NOTHING, 
        db_comment='The course selection regime selected for this session.'
    )
    image_name = models.TextField(blank=True, null=True, db_comment='The name of the image file showing the selections made')

    class Meta:
        managed = False
        db_table = 'session'
        db_table_comment = 'The settings for a single VS Race session of Mario Kart. Not all settings apply to every version of the game. Does not apply to other race types (e.g. Grand Prix).\n\n  Assumes that a session is incomplete until updated, and that a session only takes place on a single calendar day.'


class PlayerSession(models.Model):
    player_session_id = models.AutoField(primary_key=True, db_comment='Primary key')
    session = models.ForeignKey(
        to=Session, 
        on_delete=models.DO_NOTHING, 
        db_comment='The session to which this setup applies.'
    )
    player = models.ForeignKey(
        to=Player, 
        on_delete=models.DO_NOTHING, 
        db_comment='The player to which this setup applies.'
    )
    character = models.ForeignKey(
        to=Character, 
        on_delete=models.DO_NOTHING, 
        db_comment='The character selected by the player in this session.'
    )
    vehicle = models.ForeignKey(
        to=Vehicle, 
        on_delete=models.DO_NOTHING, 
        db_comment='The vehicle selected by the player in this session.'
    )
    wheel = models.ForeignKey(
        to=Wheel, 
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True, 
        db_comment='The wheels selected by the player for this session. MK 8 only.'
    )
    glider = models.ForeignKey(
        to=Glider, 
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True, 
        db_comment='The glider selected by the player for this session. MK 8 only.'
    )

    class Meta:
        managed = False
        db_table = 'player_session'
        unique_together = (('session', 'player'),)
        db_table_comment = 'Selections made by a player during session setup. Selections from the `player_default` table will be re-entered, rather than inserting a reference.'


class Race(models.Model):
    race_id = models.AutoField(primary_key=True, db_comment='Primary key')
    session = models.ForeignKey(
        to=Session, 
        on_delete=models.DO_NOTHING, 
        db_comment='The session of which the race is a part'
    )
    race_no = models.IntegerField(db_comment='The race number within the session')
    start_track_id = models.ForeignKey(
        to=Track, 
        related_name='as_start_track',
        db_column='start_track_id',
        on_delete=models.DO_NOTHING, 
        db_comment='The starting track of the race (MK World) or the track on which the race is done (MK 8)',
    )
    end_track_id = models.ForeignKey(
        to=Track, 
        related_name='as_end_track',
        db_column='end_track_id',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        db_comment='The ending track of the race. MK World only.'
    )

    class Meta:
        managed = False
        db_table = 'race'
        unique_together = (('session', 'race_no'),)
        db_table_comment = 'Stores the details of each race within a session. \n  \n  For Mario Kart 8, only `start_track_id` should be completed. For Mario Kart World, `end_track_id` may be null (indicates that it was a single-track race).'


class RaceResult(models.Model):
    race_result_id = models.AutoField(primary_key=True, db_comment='Primary key')
    race = models.ForeignKey(
        to=Race, 
        on_delete=models.DO_NOTHING, 
        db_comment='The race for which this result is for'
    )
    player = models.ForeignKey(
        to=Player, 
        on_delete=models.DO_NOTHING, 
        db_comment='The player for which this result is for'
    )
    position = models.ForeignKey(
        to=Position, 
        on_delete=models.DO_NOTHING, 
        db_comment='The position in which the player finished.'
    )

    class Meta:
        managed = False
        db_table = 'race_result'
        unique_together = (('race', 'player'),)
        db_table_comment = 'Stores the results of races for each player. Given that positions are tied to points, a foreign key relationship is required."'
