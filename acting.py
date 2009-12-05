# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from hce import check_action, GUARANTEED_ROLL, max_influence, max_recovery, \
    ROLL_EFFECT
from model import INFLUENCES
import random

def flow(self, subject=None, **kwargs):
    if not self._char(subject): return False
    if not self._active(): return False

    for inf in INFLUENCES:
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
    cando, is_guaranteed = check_action(self.char, False, influence, heroic,
        profession)
    if not cando:
        self.errors.append('%s does not have enough will exerted to perform.' %
            self.char.name)
        return
    if is_guaranteed:
        self.game.lastroll = GUARANTEED_ROLL
    else:
        self.game.lastroll = random.randint(0, 9)
    inf = getattr(self.char, influence)
    maxinf = max_influence(self.char, influence)
    if inf > maxinf:
        # Excess influence is "spent"
        setattr(self.char, influence, maxinf)
        self.char.will_spent += maxinf - inf
        if self.char.key() not in self.updated:
            self.updated.append(self.char.key())
    self.game.cureffect, self.game.curtiming = ROLL_EFFECT[self.game.lastroll]
    self.gameupdated = True

def contest(self, subject=None, influence=None, heroic=None, profession=None,
        object=None, **kwargs):
    if not self._char(subject): return False
    if not self._active(): return False

    # TODO: Use the object, for potential defense

    self.game.lastinfluence = influence
    cando, is_guaranteed = check_action(self.char, True, influence, heroic,
        profession)
    if not cando:
        self.errors.append('%s does not have enough will exerted to perform.' %
            self.char.name)
        return
    if is_guaranteed:
        self.game.lastroll = GUARANTEED_ROLL
    else:
        self.game.lastroll = random.randint(0, 9)
    inf = getattr(self.char, influence)
    maxinf = max_influence(self.char, influence)
    if inf > maxinf:
        # Excess influence is "spent"
        setattr(self.char, influence, maxinf)
        self.char.will_spent += maxinf - inf
        if self.char.key() not in self.updated:
            self.updated.append(self.char.key())
    self.game.cureffect, self.game.curtiming = ROLL_EFFECT[self.game.lastroll]
    self.gameupdated = True

def lose(self, subject=None, count=0, **kwargs):
    if not self._char(subject): return False
    if not self._active(): return False

    tokens = min(self.char.ego, count)
    self.char.ego -= tokens
    self.char.ego_spot += tokens
    if tokens < count:
        self.warnings.append('%s had fewer than %s ego left.' % (
            self.char.name, count))
    if self.char.ego == 0:
        self.char.active = False
        if self.char in self._activechars:
            self._activechars.remove(self.char)
        self.warnings.append('%s has passed out.' % self.char.name)
    if self.char.key() not in self.updated:
        self.updated.append(self.char.key())

def recover(self, subject=None, count=None, what=None, **kwargs):
    if not self._char(subject): return False
    if not self._active(): return False

    mr = max_recovery(self.char)
    if count is not None and count > mr:
        self.warnings.append("%s is greater than %s's expected maximum recovery (%s)." % (
            count, self.char.name, mr))
    elif count is None:
        count = mr

    if what is None:
        tokens = min(self.char.will_spent, count)
        self.char.will_spent -= tokens
        self.char.will += tokens
        if count > tokens:
            what = 'ego'
            count -= tokens
    if what == 'ego':
        tokens = min(self.char.ego_spot, count)
        self.char.ego_spot -= tokens
        self.char.ego += tokens
    elif what == 'will':
        tokens = min(self.char.will_spent, count)
        self.char.will_spent -= tokens
        self.char.will += tokens
    if self.char.key() not in self.updated:
        self.updated.append(self.char.key())

# vim: ai et ts=4 sts=4 sw=4
