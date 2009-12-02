# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from models import SPOTS

"""
This is a module for HCE-specific domain knowledge.
"""

TIME_READY = 9

# Professions range between 0 and 3 tokens
in_prof_range = lambda x: x >= 0 and x <= 3

# Spots modified by the "has" verb
in_spot_range = {}
for spot in SPOTS:
    if spot in ('ego', 'will', 'ego_spot', 'will_spot'):
        in_spot_range[spot] = lambda x: x >= 0 and x <= 100
    else:
        in_spot_range[spot] = lambda x: x >= 0 and x <= 3

def tick(time):
    if time != 0:
        time += 1
        if time > 6:
            time = TIME_READY
        return time
    else:
        return 0

# vim: ai et ts=4 sts=4 sw=4
