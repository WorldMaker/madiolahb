# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from google.appengine.ext import db

class Character(db.Model):
    owner = db.StringProperty(required=True)
    name = db.StringProperty()
    # Source
    ego = db.IntegerProperty(required=True)
    will = db.IntegerProperty(required=True)
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

# vim: ai ts=4 sts=4 et sw=4
