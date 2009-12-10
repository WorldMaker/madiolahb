# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from models import SPOTS

"""
This is a module for HCE-specific domain knowledge.
"""

TIME_READY = 9
GUARANTEED_ROLL = 6

INFLUENCE_ELEMENTS = {
    'body': ('earth', 'air'),
    'mind': ('water', 'fire'),
    'spirit': ('life', 'energy'),
    'mastery': ('life', 'earth'),
    'persistence': ('earth', 'water'),
    'design': ('water', 'energy'),
    'poise': ('energy', 'air'),
    'sleight': ('air', 'fire'),
    'charm': ('fire', 'life'),
}

ROLL_EFFECT = {
    0: (-5, -6),
    1: (-4, -3),
    2: (-3, -2),
    3: (0, -1),
    4: (0, 0),
    5: (0, 1),
    6: (3, 1),
    7: (4, 2),
    8: (5, 3),
    9: (6, 6),
}

# (Heroic, Contested) -> (Will Needed, Will to Guarantee)
ACTION_WILL = {
    (False, False): (0, 1),
    (False, True): (1, 3),
    (True, False): (2, 5),
    (True, True): (3, 7),
}

# Professions range between 0 and 3 tokens
in_prof_range = lambda x: x >= 0 and x <= 3

# Spots modified by the "has" verb
in_spot_range = {}
for spot in SPOTS:
    if spot in ('ego', 'will', 'ego_spot', 'will_spot'):
        in_spot_range[spot] = lambda x: x >= 0 and x <= 100
    else:
        in_spot_range[spot] = lambda x: x >= 0 and x <= 3

time_range = lambda time: time >= 0 and (time <= 6 or time == 9)

def tick(time):
    if time != 0:
        time += 1
        if time > 6:
            time = TIME_READY
        return time
    else:
        return 0

def max_influence(char, influence):
    """
    Returns the maximum will that can safely be "exerted" through a
    given influence.
    """
    ele0, ele1 = INFLUENCE_ELEMENTS[influence]
    return min(1, getattr(char, ele0, 0) + getattr(char, ele1, 0))

def my_effected_time(char, influence, timingeffect):
    """
    Given the action's influence and timingeffect, provide the default
    time value to reset to.
    """
    time = max(0, min(7, max_influence(char, influence) + timingeffect))
    if time == 7: time = 9
    return time

def other_effected_time(time, timingeffect):
    """
    Given the current time of some other character and the timingeffect,
    provide the default time value to reset to, and any leftover effect.
    """
    if timingeffect == -6:
        return 9, 0
    totaltime = time + timingeffect
    actualtime = max(0, min(7, totaltime))
    delta = abs(totaltime - actualtime)
    return actualtime, delta

def check_action(char, contested, influence, heroic, profession):
    will, gua = ACTION_WILL[heroic, contested]
    avail = getattr(char, influence, 0) + getattr(char, 'job%s' % profession, 0)
    return avail >= will, avail >= gua

def max_recovery(char):
    return max(char.energy, 1)

# vim: ai et ts=4 sts=4 sw=4
