This file outlines the datasets in the old Mario Kart Tracker system and how they map to the data in the new system.

# Tables

| Sheet Name | Table Name |
|------------|------------|
| VS | `session` |
| VS Config | `player_session` |
| Result | `race`, `race_result` |

The sheets Tracks, Vehicles, Wheels, Gliders, and Points all map directly onto the database. 

The defaults won't be migrated. This is because the player configuration is saved each time, (defaults are used to prefill. A reference isn't saved) so only the Config for each player session needs to be migrated. 

The points table doesn't need migrating, as the values already exist in the database and there won't be any text differences.

The Player sheet won't be migrated, given that the data is exactly the same.

# Columns

## VS

| Sheet Column | Database Column | Note |
|--------------|-----------------|------|
| vs_id | - | - |
| cc | `engine_class.name` &rarr; `session.engine_class_id` | - |
| track_choice | `course_selection.name` &rarr; `session.course_selection_id`| - |
| races | `session.no_races` | - |
| date | `session.play_date` | The sheets only contain date information, not time. The times will default to 00:00:00 |

### Calculated and Default Values

| Database Column | Value | Note |
|-----------------|---------|------|
| `session_id` | - | - |
| `no_players` | 2 | A count in the sheet showed that all sessions had 2 players| 
| `game_version_id` | "Mario Kart 8 Deluxe" | `game_version_id` selected from DB |
| `play_date` |  | - |
| `is_complete` | `TRUE` | The old system only saved results if the session was finished, so there won't be any unfinished sessions |
| `no_races` |  | - |
| `engine_class_id` |  | - |
| `teams` | 0 | - |
| `item_rule_id` | "Frantic" | `item_rule_id` selected from DB |
| `cpu_difficulty_id` | "Hard" | `cpu_difficulty_id` selected from DB |
| `vehicle_selection_id` | "All" | `vehicle_selection_id` selected from DB |
| `course_selection_id` |  | - |
| `image_name` | `NULL` | - |

## VS Config

| Sheet Column | Database Column | Note |
|--------------|-----------------|------|
| Config ID | - | - |
| VS ID | - | - |
| Player | `player.name` &rarr; `session.player_id` | - |
| Character | `character.name` &rarr; `session.character_id` | - |
| Vehicle | `vehicle.name` &rarr; `session.vehicle_id` | - |
| Wheels | `wheel.name` &rarr; `session.wheel_id` | - |
| Glider | `glider.name` &rarr; `session.glider_id` | - |

### Calculated and Default Values

| Database Column | Value | Note |
|-----------------|---------|------|
| `player_session_id` | - | - |
| `session_id` | Mapping of VS sheet ID to DB's ID | - |
| `player_id` | - | - |
| `character_id` | - | - |
| `vehicle_id` | - | - |
| `wheel_id` | - | - |
| `glider_id` | - | - |

## Result

Result will be split over 2 tables: `race` and `race_result`.

Result ID is most similar to `race_result_id`, which means that races don't have a unique identifier for mapping. We'll need to address this by making a temporary pseudo-id.

| Sheet Column | Database Column | Note |
|--------------|-----------------|------|
| Result ID | - | - |
| VS ID | - | - |
| Race No | `race.race_no` | - |
| Track | `track.name` &rarr; `race.start_track_id` | - |
| Config ID | - | - |
| Pos | `position.position` &rarr; `race_result.position_id` | - |

### Calculated and Default Values

`race`

| Database Column | Value | Note |
|-----------------|---------|------|
| `race_id` | Generated id for each unique race | - |
| `session_id` | Mapping of VS sheet ID to DB's ID |  |
| `race_no` | - | - |
| `start_track_id` | - | - |
| `end_track_id` | `NULL` | - |

`race_result`

| Database Column | Value | Note |
|-----------------|---------|------|
| `race_result_id` | - | - |
| `race_id` | Mapping of a pseudo-id to `race.race_id` |  |
| `player_session_id` | Mapping of VS Config sheet ID to DB's `player_session_id` |  |
| `position_id` | `position.position` &rarr; `race_result.position_id` | - |