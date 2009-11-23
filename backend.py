from parser import NoMatch, parse
from models import Character

class Commander(object):
    """
    The commander is the backend that takes given commands and
    applies them to the data model (producing errors and warnings
    when and as necessary).
    """
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
                self.asclause = sentence["as"]
            verb = getattr(self, sentence["verb"], self.unimplemented_verb)
            status = verb(**sentence)
            if status is not None and not status: return status

    def playing(self, subject=None, name='', **kwargs):
        # Check for an existing character with this name
        exists = Character.all().ancestor(self.game).filter('name =', name) \
            .count(1)
        if exists:
            self.errors.append('Character name exists: %s' % name)
            return False
        owner = self.sender
        if subject is not None:
            if isinstance(subject, basestring):
                self.warnings.append('The subject of "is playing" should be a player.')
            elif subject.type == 'Addr':
                owner = subject.value
        self.char = self.game.new_char(owner, name)

# vim: ai et ts=4 sts=4 sw=4
