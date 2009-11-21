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
            verb = getattr(self, sentence["verb"], self.unimplemented_verb)
            verb(**sentence)

# vim: ai et ts=4 sts=4 sw=4
