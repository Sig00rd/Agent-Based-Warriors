RED_MOVEMENT_SPEED = 0.1
BLUE_MOVEMENT_SPEED = 0.1

COHERENCE_FACTOR = 0.025
SEPARATION_FACTOR = 0.2
MATCH_FACTOR = 0.05
ENEMY_POSITION_FACTOR = 0.03

VISION_RANGE = 50
FLOCKING_RADIUS = 5
SEPARATION_DISTANCE = 1

#
ALLIES_MORALE_WEIGHT = 0.4

def kill_morale_modifier(has_killed: bool) -> float:
    if has_killed:
        return 10
    return 0

def damage_inflicted_morale_modifier(damage_inflicted: float) -> float:
    return damage_inflicted

def damage_received_morale_modifier(damage_received_recently: float, initial_hp: float) -> float:
    return damage_received_recently.__pow__(2) / initial_hp

SEPARATION_DISTANCE = 1.5