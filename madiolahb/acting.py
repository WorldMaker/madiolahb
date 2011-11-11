# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from core import check_action, GUARANTEED_ROLL, INFLUENCES, max_influence,
    max_recovery, ROLL_EFFECT
import random

def exert(char, **kwargs):
    """
    Lifewheel will is exerted to perform actions.
    """
    for inf in INFLUENCES:
        if inf in kwargs:
            if char['will'] < kwargs[inf]:
                char['warnings'].append('Not enough will to move %s to %s' % (
                    kwargs[inf], inf))
            else:
                maxinf = max_influence(self.char, inf)
                if kwargs[inf] > maxinf:
                    char['warnings'].append('Over-exerted: %s > %s' % (
                        kwargs[inf], maxinf))
                char['will'] -= kwargs[inf]
                char[inf] = char[inf] + kwargs[inf]

def act(char, influence=None, domain=False, profession=None, **kwargs):
    """
    Performing an unopposed action
    """
    char['last_influence'] = influence
    cando, is_guaranteed = check_action(char, False, influence, heroic,
        profession)
    if not cando:
        char['errors'].append('%s does not have enough will exerted to perform.' %
            char['name'])
        return
    if is_guaranteed:
        self.game.lastroll = GUARANTEED_ROLL
    else:
        self.game.lastroll = random.randint(0, 9)
    inf = char['influence']
    maxinf = max_influence(char, influence)
    if inf > maxinf:
        # Excess influence is "spent"
        char['influence'] = maxinf
        char['will_spent'] += maxinf - inf
    self.game.cureffect, self.game.curtiming = ROLL_EFFECT[self.game.lastroll]

def contest(char, influence=None, heroic=None, profession=None,
        object=None, **kwargs):

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

def lose(char, count=0, **kwargs):
    """
    Sometimes lifewheels lose ego when performances are unfavorable.
    """
    tokens = min(self.char.ego, count)
    char['ego'] -= tokens
    char['ego_spilt'] += tokens
    if tokens < count:
        chars['warnings'].append('%s had fewer than %s ego left.' % (
            char['name'], count))
    if char['ego'] <= 0:
        char['ego'] = 0
        char['active'] = False
        char['warnings'].append('%s has passed out.' % char['name'])

def recover(char, count=None, what=None, **kwargs):
    """
    Eventually lifewheels recover
    """
    mr = max_recovery(char)
    if count is not None and count > mr:
        char['warnings'].append("%s is greater than %s's expected maximum recovery (%s)." % (
            count, char['name'], mr))
    elif count is None:
        count = mr

    if what is None:
        tokens = min(char['will_spent'], count)
        char['will_spent'] -= tokens
        char['will'] += tokens
        if count > tokens:
            what = 'ego'
            count -= tokens
    if what == 'ego':
        tokens = min(char['ego_spilt'], count)
        char['ego_spilt'] -= tokens
        char['ego'] += tokens
    elif what == 'will':
        tokens = min(char['will_spent'], count)
        char['will_spent'] -= tokens
        char['will'] += tokens

# vim: ai et ts=4 sts=4 sw=4
