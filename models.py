# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

# These are the spots used by the "has" verb
SPOTS = ('ego', 'will', 'ego_spot', 'will_spot', 'life', 'earth', 'water',
    'energy', 'air', 'fire', 'will_spent')

INFLUENCES = ('mastery', 'persistence', 'design', 'poise', 'sleight',
    'charm', 'mind', 'body', 'spirit')

class Character(db.Model):
    owner = db.StringProperty(required=True)
    name = db.StringProperty()
    active = db.BooleanProperty(default=True)
    # Source
    ego = db.IntegerProperty(default=0)
    will = db.IntegerProperty(default=0)
    # "Drained" Spots
    ego_spot = db.IntegerProperty(default=0)
    will_spot = db.IntegerProperty(default=0)
    will_spent = db.IntegerProperty(default=0)
    # Elements of Ego
    life = db.IntegerProperty(default=0)
    earth = db.IntegerProperty(default=0)
    water = db.IntegerProperty(default=0)
    # Elements of Will
    energy = db.IntegerProperty(default=0)
    air = db.IntegerProperty(default=0)
    fire = db.IntegerProperty(default=0)
    # Professions
    job1 = db.IntegerProperty(default=0)
    job2 = db.IntegerProperty(default=0)
    job3 = db.IntegerProperty(default=0)
    # Time Track
    time = db.IntegerProperty(default=0)
    recovery = db.IntegerProperty(default=0) # 0s and 9s until can move 0 -> 1
    # Mundane Influences
    mastery = db.IntegerProperty(default=0) # life, earth
    persistence = db.IntegerProperty(default=0) # earth, water
    design = db.IntegerProperty(default=0) # water, energy
    poise = db.IntegerProperty(default=0) # energy, air
    sleight = db.IntegerProperty(default=0) # air, fire
    charm = db.IntegerProperty(default=0) # fire, life
    # Heroic Influences
    mind = db.IntegerProperty(default=0)
    body = db.IntegerProperty(default=0)
    spirit = db.IntegerProperty(default=0)
    # "Position" (Presumably Hex Map Coordinates)
    x = db.IntegerProperty(default=0)
    y = db.IntegerProperty(default=0)

class Game(polymodel.PolyModel):
    title = db.StringProperty()
    players = db.StringListProperty()
    hold = db.ListProperty(db.Key) # Explicit holding chars
    # Current "active" char
    active = db.ReferenceProperty(Character,
        collection_name='active_in_game_set')
    lastinfluence = db.StringProperty()
    lastroll = db.IntegerProperty()
    cureffect = db.IntegerProperty() # Current effect taken by active char
    curtiming = db.IntegerProperty() # Current timing taken by active char
    renownvote = db.BooleanProperty(default=False)
    renownnom = db.ReferenceProperty(Character,
        collection_name='renown_nominated_set')
    renowninf = db.StringProperty()
    renowncount = db.IntegerProperty()
    renownaye = db.StringListProperty()
    renownnay = db.StringListProperty()
    hexmap = db.BooleanProperty(default=True)

    @property
    def active_chars(self):
        return Character.all().ancestor(self).filter('active =', True)

    def new_char(self, owner, name, **kwargs):
        return Character(parent=self,
            owner=owner,
            name=name,
            **kwargs
        )

class WaveGame(Game):
    waveid = db.StringProperty(required=True)

class EmailGame(Game):
    pass

class XmppGame(Game):
    pass

class Channel(db.Model):
    """
    A Channel moderates Email and Xmpp games.
    """
    owner = db.UserProperty(required=True)
    active_email_game = db.ReferenceProperty(EmailGame,
        collection_name='active_set')
    active_xmpp_game = db.ReferenceProperty(XmppGame,
        collection_name='active_set')
    games = db.ReferenceProperty(Game)

# vim: ai ts=4 sts=4 et sw=4
