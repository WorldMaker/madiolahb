# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from hce import is_guaranteed, GUARANTEED_ROLL, ROLL_EFFECT
from model import INFLUENCES
import random

def flow(self, subject=None, **kwargs):
    if not self._char(subject): return False
    if not self._active(): return False

    for inf in INFLUENCE:
        if inf in kwargs:
            if self.char.will < kwargs[inf]:
                self.warnings.append('Not enough will to move %s to %s' % (
                    kwargs[inf], inf))
            else:
                self.char.will -= kwargs[inf]
                oldinfcount = getattr(self.char, inf)
                setattr(self.char, inf, oldinfcount + kwargs[inf])
                if self.char.key() not in self.updated:
                    self.updated.append(self.char.key())

def act(self, subject=None, influence=None, heroic=None, profession=None,
        **kwargs):
    if not self._char(subject): return False
    if not self._active(): return False

    self.game.lastinfluence = influence
    if is_guaranteed(self.char, False, influence, heroic, profession):
        self.game.lastroll = GUARANTEED_ROLL
    else:
        self.game.lastroll = random.randint(0, 9)
    self.game.cureffect, self.game.curtiming = ROLL_EFFECT[self.game.lastroll]
    self.gameupdated = True

def contest(self, subject=None, influence=None, heroic=None, profession=None,
        object=None, **kwargs):
    if not self._char(subject): return False
    if not self._active(): return False

    # TODO: Use the object, for potential defense

    self.game.lastinfluence = influence
    if is_guaranteed(self.char, True, influence, heroic, profession):
        self.game.lastroll = GUARANTEED_ROLL
    else:
        self.game.lastroll = random.randint(0, 9)
    self.game.cureffect, self.game.curtiming = ROLL_EFFECT[self.game.lastroll]
    self.gameupdated = True

# vim: ai et ts=4 sts=4 sw=4
