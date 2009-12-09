# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from models import Character
from parser import NoMatch, parse, Special
import re

COMMAND_RE = re.compile(r'\[\s*(?P<commands>[^\]]+\.)\s*\]')

# Command imports
from chardesc import advanced, has, playing
from timecommands import _crit, set, _tick, timing
from acting import act, contest, flow, lose, recover
from movement import at, move
from renown import renown, vote
from charcommands import activate, chown, deactivate

class Commander(object):
    """
    The commander is the backend that takes given commands and
    applies them to the data model (producing errors and warnings
    when and as necessary).
    """
    # Character description commands
    advanced = advanced
    has = has
    playing = playing
    # Timing commands
    _crit = _crit
    set = set
    _tick = _tick
    timing = timing
    # Acting commands
    act = act
    contest = contest
    flow = flow
    lose = lose
    recover = recover
    # Movement commands
    at = at
    move = move
    # Renown commands
    renown = renown
    vote = vote
    # Character meta commands
    activate = activate
    chown = chown
    deactivate = deactivate

    def __init__(self, game=None, sender=None):
        """
        Sender and game are expected from the front-end, for the most
        part.
        """
        self.game = game
        self.sender = sender
        self.asclause = None
        self.char = None
        self.errors = []
        self.warnings = []
        self.gameupdated = False
        self.updated = [] # Objects that should be db.put
        self.charcache = {}
        self._activechars = []
        self.commanded = [] # "Accepted" command sentences
        self.atready = []
        self.tickselapsed = 0

    def unimplemented_verb(self, verb='', **kwargs):
        self.errors.append('Unimplemented verb "%s"' % verb)

    def command(self, input):
        self.errors = []
        self.warnings = []
        self.commanded = []
        self.atready = []
        self.tickselapsed = 0
        try:
            sentences = parse(input)
        except NoMatch, e:
            self.errors.append('While parsing: expected %s at position %s'
                % (e.value, e.parser.pos_to_linecol(e.position)))
            return False
        for sentence in sentences:
            if not sentence["imsentence"] and not self.game:
                self.errors.append('Not in a game.')
                return False
            if "as" in sentence:
                self.char = None
                self.asclause = sentence["as"]
            verb = getattr(self, sentence["verb"], self.unimplemented_verb)
            status = verb(**sentence)
            if status is not None and not status: return status
            else:
                self.commanded.append(sentence)

    def commit(self):
        from google.appengine.ext import db
        upd = [self.charcache[k] for k in self.updated]
        if self.gameupdated:
            upd.insert(0, self.game)
        db.put(upd)
        self.gameupdated = False
        self.updated = []

    def _addrchar(self, addr):
        chars = list(Character.all().ancestor(self.game) \
            .filter('owner =', addr).fetch(2))
        if len(chars) != 1:
            char = None
            self.warnings.append('%s does not have one and only one character'
                % addr)
        else:
            char = chars[0]
            if char.key() in self.charcache:
                return self.charcache[char.key()]
        return char

    def _namechar(self, charname):
        # Check for an existing cached copy
        for char in self.charcache.values():
            if char.name == charname:
                return char
        char = Character.all().ancestor(self.game) \
            .filter('name =', charname).get()
        self.charcache[char.key()] = char
        return char

    @property
    def activechars(self):
        if not self._activechars:
            self._activechars = []
            achars = list(self.game.active_chars)
            for char in achars:
                if char.key() in self.charcache:
                    self._activechars.append(self.charcache[char.key()])
                else:
                    self.charcache[char.key()] = char
                    self._activechars.append(char)
        return self._activechars

    def _char(self, subject=None):
        # Explicit character in the subject or as clause
        if (isinstance(subject, basestring)
        or (isinstance(self.asclause, basestring)
        and (subject is None or subject.type == 'Pronoun'))):
            charname = subject
            if not charname or not isinstance(charname, basestring):
                # Try looking up the as clause, but only if no current char
                if self.char is not None:
                    return self.char
                charname = self.asclause
            char = self._namechar(charname)
            if char:
                if char.owner == self.sender:
                    self.char = char
                else:
                    # Explicit "as someotheruser@example.com," clause
                    if (isinstance(self.asclause, Special)
                    and self.asclause.type == 'Addr'
                    and self.asclause.value == char.owner):
                        self.char = char
                    else:
                        self.char = None
                        self.errors.append('%s should not be playing for %s' % (
                            self.sender, charname))
            else:
                self.char = None
                self.errors.append("Can't find character named %s" % charname)
        # One-And-Only-One character lookup
        elif (isinstance(subject, Special)
        and subject.type == 'Addr') or self.char is None:
            addr = self.sender
            if isinstance(subject, Special) and subject.type == 'Addr':
                addr = subject.value
            elif (isinstance(self.asclause, Special)
            and self.asclause.type == 'Addr'):
                addr = self.asclause.value
            self.char = self._addrchar(addr)
        return self.char

    def _active(self):
        if self.char.name == self.game.active:
            return True
        else:
            self.warnings.append('%s is not currently active' % self.char.name)
            return False

    def _object(self, object=None):
        if object is None or (isinstance(object, Special)
        and object.type == 'Pronoun'):
            return self.char
        elif isinstance(object, Special) and object.type == 'Addr':
            return self._addrchar(object.value)
        else:
            return self._namechar(object)

# vim: ai et ts=4 sts=4 sw=4
