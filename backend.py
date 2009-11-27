# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from models import Character
from parser import NoMatch, parse, Special

# Command imports
from chardesc import advanced, has, playing

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
        self.updated = [] # Objects that should be db.put

    def unimplemented_verb(self, verb='', **kwargs):
        self.errors.append('Unimplemented verb "%s"' % verb)

    def command(self, input):
        self.errors = []
        self.warnings = []
        try:
            sentences = parse(input)
        except NoMatch, e:
            self.errors.append('While parsing: expected %s at position %s'
                % (e.value, e.parser.pos_to_linecol(e.position)))
            return
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

    def commit(self):
        from google.appengine.ext import db
        db.put(self.updated)
        self.updated = []

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
            char = Character.all().ancestor(self.game) \
                .filter('name =', charname).get()
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
            chars = list(Character.all().ancestor(self.game)
                .filter('owner =', addr).fetch(2))
            if len(chars) != 1:
                self.char = None
                self.errors.append('%s does not have one and only one character'
                    % addr)
            else:
                self.char = chars[0]
        return self.char

# vim: ai et ts=4 sts=4 sw=4
