=======================
Madiolahb JSON Schemata
=======================

Madiolahb promotes a simple JSON schema for interacting with and/or
interchanging Bhaloidam data.

The formats themselves are meant to be self-documenting and easy to implement
given a reasonable familiarity with Bhaloidam. This document serves to present
the formats in a simple overview and to provide a place for any necessary
further disambiguation. This document, as all Madiolahb documents, is CC
by-sa, but the formats presented here in any such aspects as may be
deemed copyrightable are open for use under CC0 or other such similar
public domain right or license.

Lifewheel
=========

The *Lifewheel* format (referred at times in Madiolahb as "Character" or
"Char" format) is of course the central data structure in Madiolahb.

.. todo::

   Either elaborate why the "Character" name remains in use in madiolahb
   or clean those up.

.. sourcecode:: js

   {
       // Madiolahb metadata
       'owner': 'test@example.com',
       'name': 'Name of this Life Wheel',
       'active': true, // Currently involved in play

       // Source Values
       'ego': 0,
       'will': 0,

       // "Drained" Spots // TODO: 11-10-24 Update these names
       'ego_spot': 0,
       'will_spot': 0,
       'will_spent': 0,
       
       // Elements of Ego
       'life': 0,
       'earth': 0,
       'water': 0,

       // Elements of Will
       'energy': 0,
       'air': 0,
       'fire': 0,

       // Professions
       'job1': 0,
       'job2': 0,
       'job3': 0,

       // Time Track
       'time': 0,
       'recovery': 0, // TODO: What does this mean, again?

       // Mundane Influences
       'mastery': 0,
       'persistence': 0,
       'design': 0,
       'poise': 0,
       'sleight': 0,
       'charm': 0,

       // Heroic Influences
       'mind': 0,
       'body': 0,
       'spirit': 0,

       // Position, Presumably Hex Map Coordinates
       'x': 0,
       'y': 0
    }

.. vim: ai spell tw=72
