# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from google.appengine.ext import db

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

class GameMixin(object):
    def new_char(self, owner, name, **kwargs):
        return Character(parent=self,
            owner=owner,
            name=name,
            **kwargs
        )

class WaveGame(db.Model, GameMixin):
    waveid = db.StringProperty(required=True)

class EmailGame(db.Model, GameMixin):
    players = db.StringListProperty() # Hmm...
    subject = db.StringProperty(required=True)

class XmppGame(db.Model, GameMixin):
    players = db.StringListProperty() # Hmm...
    name = db.StringProperty(required=True)

# vim: ai ts=4 sts=4 et sw=4
