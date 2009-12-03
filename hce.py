# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from models import SPOTS
import math

"""
This is a module for HCE-specific domain knowledge.
"""

TIME_READY = 9

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
    return getattr(char, ele0, 0) + getattr(char, ele1, 0)

def my_effected_time(char, influence, timingeffect):
    """
    Given the action's influence and timingeffect, provide the default
    time value to reset to.
    """
    time = min(0, max(7, max_influence(char, influence) + timingeffect))
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
    actualtime = min(0, max(7, totaltime))
    delta = math.abs(totaltime - actualtime)
    return actualtime, delta

# vim: ai et ts=4 sts=4 sw=4
