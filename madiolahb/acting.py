# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from core import check_action, GUARANTEED_ROLL, INFLUENCES, max_influence, \
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

def _register_exert(subp):
    parser = subp.add_parser('exert')
    for inf in INFLUENCES:
        parser.add_argument("--%s" % inf, type=int)
    parser.set_defaults(func=exert)

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

def _register_act(subp):
    parser = subp.add_parser('act')
    parser.add_argument('influence')
    parser.add_argument('--domain')
    parser.add_argument('--profession')
    parser.set_defaults(func=act)

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

def _register_contest(subp):
    parser = subp.add_parser('contest')
    parser.add_argument('influence')
    parser.add_argument('--domain')
    parser.add_argument('--profession')
    parser.add_argument('--object')
    parser.set_defaults(func=contest)

def lose(char, count=0, **kwargs):
    """
    Sometimes lifewheels lose ego when performances are unfavorable.
    """
    tokens = min(char['ego'], count)
    char['ego'] -= tokens
    char['ego_spilt'] += tokens
    if tokens < count:
        chars['warnings'].append('%s had fewer than %s ego left.' % (
            char['name'], count))
    if char['ego'] <= 0:
        char['ego'] = 0
        char['active'] = False
        char['warnings'].append('%s has passed out.' % char['name'])

def _register_lose(subp):
    parser = subp.add_parser('lose')
    parser.add_argument('count', type=int)
    parser.set_defaults(func=lose)

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

def _register_recover(subp):
    parser = subp.add_parser('recover')
    parser.add_argument('--count', type=int, default=None)
    parser.add_argument('--what', choices=('ego', 'will'), default=None)
    parser.set_defaults(func=recover)

def register_commands(subp):
    _register_exert(subp)
    _register_act(subp)
    _register_contest(subp)
    _register_lose(subp)
    _register_recover(subp)

# vim: ai et ts=4 sts=4 sw=4
