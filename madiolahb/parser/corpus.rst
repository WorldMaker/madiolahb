Language Corpus
===============

:Copyright: 2009 Max Battcher. Some Rights Reserved (CC by-sa).

This is a collection of doctests to test that sentences in the language
parse as expected.

Character Description
---------------------

Creating a character::

  >>> sen = parse('I am playing the pope.')[0]
  >>> sen['subject'], sen['verb'], sen['name']
  (Pronoun, 'playing', 'the pope')

  >>> sen = parse('rob@gwave.example.com is playing Clown.')[0]
  >>> sen['subject'], sen['verb'], sen['name']
  (Addr: rob@gwave.example.com, 'playing', 'clown')

Setting a character's professional advancement::

  >>> sen = parse('I have advanced to 3 in profession 1.')[0]
  >>> sen['verb'], sen['prof1']
  ('advanced', 3)

  >>> sen = parse('I advanced 3 in my first profession.')[0]
  >>> sen['verb'], sen['prof1']
  ('advanced', 3)

  >>> sen = parse('I advanced 2 in profession 2, 3 in profession 1, and 1 in my third profession.')[0]
  >>> sen['verb'], sen['prof1'], sen['prof2'], sen['prof3']
  ('advanced', 3, 2, 1)

  >>> sen = parse('Advanced 3 in my first profession.')[0]
  >>> sen['verb'], sen['prof1']
  ('advanced', 3)

Setting a character's spots::

  >>> sen = parse('I have 3 will.')[0]
  >>> sen['verb'], sen['will']
  ('has', 3)

  >>> sen = parse('I have 3 will drained.')[0]
  >>> sen['verb'], sen['will_spot']
  ('has', 3)

  >>> sen = parse('I have 3 will and 4 ego, 1 will drained and 3 life.')[0]
  >>> sen['verb'], sen['will'], sen['will_spot'], sen['ego'], sen['life']
  ('has', 3, 1, 4, 3)

  >>> sen = parse('I have 2 will spent and 1 ego spent.')[0]
  >>> sen['verb'], sen['will_spent'], sen['ego_spot']
  ('has', 2, 1)

  >>> sen = parse('I have 1 Water, 2 Energy, 1 Air, 2 Fire.')[0]
  >>> sen['verb'], sen['water'], sen['energy'], sen['air'], sen['fire']
  ('has', 1, 2, 1, 2)

Game Flow
---------

Timing verbs::

  >>> sen = parse('Ready.')[0]
  >>> sen['subject'], sen['verb'], sen['value']
  (None, 'timing', 'ready')

  >>> sen = parse('I ready.')[0]
  >>> sen['subject'], sen['verb'], sen['value']
  (Pronoun, 'timing', 'ready')

  >>> sen = parse('He readies.')[0]
  >>> sen['subject'], sen['verb'], sen['value']
  (Pronoun, 'timing', 'readies')

  >>> sen = parse('I hold.')[0]
  >>> sen['subject'], sen['verb'], sen['value']
  (Pronoun, 'timing', 'hold')

  >>> sen = parse('I interrupt.')[0]
  >>> sen['subject'], sen['verb'], sen['value']
  (Pronoun, 'timing', 'interrupt')

  >>> sen = parse('The ready-made weapon holder is ready.')[0]
  >>> sen['subject'], sen['verb'], sen['value']
  ('the ready-made weapon holder', 'timing', 'ready')

Exerting influence::

  >>> sen = parse('I flow 1 to poise.')[0]
  >>> sen['verb'], sen['poise']
  ('flow', 1)

  >>> sen = parse('He exerts 2 to charm.')[0]
  >>> sen['verb'], sen['charm']
  ('flow', 2)

  >>> sen = parse('I exert 1 to mastery and 2 to sleight.')[0]
  >>> sen['verb'], sen['mastery'], sen['sleight']
  ('flow', 1, 2)

  >>> sen = parse('Flow 1 to design.')[0]
  >>> sen['verb'], sen['design']
  ('flow', 1)

Unchallenged actions::

  >>> sen = parse('I act with poise.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('act', 'poise', False, 0)

  >>> sen = parse('I act with charm under my first profession.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('act', 'charm', False, 1)

  >>> sen = parse('Action with design.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('act', 'design', False, 0)

  >>> sen = parse('Action with mind mastery.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['hero_influence']
  ('act', 'mastery', True, 'mind')

  >>> sen = parse('Action with body.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['hero_influence']
  ('act', None, True, 'body')

Challenged actions::

  >>> sen = parse('I challenge Bob in poise.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('contest', 'poise', False, 0)
  >>> sen['object']
  'bob'

  >>> sen = parse('I contest against joe@example.com with charm under my first profession.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('contest', 'charm', False, 1)
  >>> sen['object']
  Addr: joe@example.com

  >>> sen = parse('Challenge Steve with design.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('contest', 'design', False, 0)
  >>> sen['object']
  'steve'

  >>> sen = parse('Challenge the Pope in sleight.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('contest', 'sleight', False, 0)
  >>> sen['object']
  'the pope'

  >>> sen = parse('Challenge Zeus with mind mastery.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['hero_influence']
  ('contest', 'mastery', True, 'mind')
  >>> sen['object']
  'zeus'

  >>> sen = parse('Challenge him with spirit.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['hero_influence']
  ('contest', None, True, 'spirit')
  >>> sen['object']
  Pronoun

Losing ego::

  >>> sen = parse('I lose 2 ego.')[0]
  >>> sen['verb'], sen['count']
  ('lose', 2)

  >>> sen = parse('I lose 1.')[0]
  >>> sen['verb'], sen['count']
  ('lose', 1)

  >>> sen = parse('Lose 3.')[0]
  >>> sen['verb'], sen['count']
  ('lose', 3)

Recovering spent will and ego::

  >>> sen = parse('I recover 3.')[0]
  >>> sen['verb'], sen['count'], sen['what']
  ('recover', 3, None)

  >>> sen = parse('He recovers 2 ego.')[0]
  >>> sen['verb'], sen['count'], sen['what']
  ('recover', 2, 'ego')

  >>> sen = parse('Recover 1 will.')[0]
  >>> sen['verb'], sen['count'], sen['what']
  ('recover', 1, 'will')

  >>> sen = parse('Recover.')[0]
  >>> sen['verb'], sen['count'], sen['what']
  ('recover', None, None)

Moving the Character
--------------------

Setup and teleport::

  >>> sen = parse('I am at 1, 2.')[0]
  >>> sen['verb'], sen['x'], sen['y']
  ('at', 1, 2)

  >>> sen = parse('He is at 3 4.')[0]
  >>> sen['verb'], sen['x'], sen['y']
  ('at', 3, 4)

  # This is ugly, but possible. Was a NoMatch at one point...
  # Was tied to another disambiguation problem...
  >>> sen = parse('It at 5 6.')[0]
  >>> sen['verb'], sen['x'], sen['y']
  ('at', 5, 6)

  >>> sen = parse('Am at 7, 8.')[0]
  >>> sen['verb'], sen['x'], sen['y']
  ('at', 7, 8)

  >>> sen = parse('At 9, 10.')[0]
  >>> sen['verb'], sen['x'], sen['y']
  ('at', 9, 10)

Movement::

  >>> sen = parse('I move to 1 spot SE.')[0]
  >>> sen['verb'], sen['dir'], sen['count'], sen['object']
  ('move', 'se', 1, None)

  >>> sen = parse('I move myself to 1 spot NE.')[0]
  >>> sen['verb'], sen['dir'], sen['count'], sen['object']
  ('move', 'ne', 1, Pronoun)

  >>> sen = parse('He moves to 2 spaces E.')[0]
  >>> sen['verb'], sen['dir'], sen['count']
  ('move', 'e', 2)

  >>> sen = parse('Move Bob the Unbearable to 8 paces NW.')[0]
  >>> sen['verb'], sen['dir'], sen['count']
  ('move', 'nw', 8)

  >>> sen = parse('Move to 3 SW.')[0]
  >>> sen['verb'], sen['dir'], sen['count']
  ('move', 'sw', 3)

Setting the Time
----------------

Resetting and otherwise setting the time track::

  >>> sen = parse('I reset.')[0]
  >>> sen['verb'], sen['time'], sen['object']
  ('set', None, None)

  >>> sen = parse('Bob sets to 1.')[0]
  >>> sen['verb'], sen['time'], sen['object']
  ('set', 1, None)

  >>> sen = parse('I set myself to 1.')[0]
  >>> sen['verb'], sen['time'], sen['object']
  ('set', 1, Pronoun)

  >>> sen = parse('I reset myself.')[0]
  >>> sen['verb'], sen['time'], sen['object']
  ('set', None, Pronoun)

  >>> sen = parse('Reset.')[0]
  >>> sen['verb'], sen['time'], sen['object']
  ('set', None, None)

  >>> sen = parse('Set to 1.')[0]
  >>> sen['verb'], sen['time'], sen['object']
  ('set', 1, None)

  >>> sen = parse('Set myself to 1.')[0]
  >>> sen['verb'], sen['time'], sen['object']
  ('set', 1, Pronoun)

  >>> sen = parse('Reset myself.')[0]
  >>> sen['verb'], sen['time'], sen['object']
  ('set', None, Pronoun)

Renown
======

Nominating renown::

  >>> sen = parse('I nominate Tom the Challenger for 1 poise renown.')[0]
  >>> sen['verb'], sen['object'], sen['influence'], sen['count']
  ('renown', 'tom the challenger', 'poise', 1)

Voting::

  >>> sen = parse('I assent.')[0]
  >>> sen['verb'], sen['value']
  ('vote', 'assent')

  >>> sen = parse('I dissent.')[0]
  >>> sen['verb'], sen['value']
  ('vote', 'dissent')

  >>> sen = parse('Aye.')[0]
  >>> sen['verb'], sen['value']
  ('vote', 'aye')

  >>> sen = parse('Nay.')[0]
  >>> sen['verb'], sen['value']
  ('vote', 'nay')

Acclimation::

  >>> sen = parse('I acclimate.')[0]
  >>> sen['verb'], sen['value']
  ('vote', 'acclimate')

  >>> sen = parse('Acclimate.')[0]
  >>> sen['verb'], sen['value']
  ('vote', 'acclimate')

Character Control
=================

Changing character ownership::

  >>> sen = parse('I yield to <jim@example.org>.')[0]
  >>> sen['verb'], sen['subject'], sen['object'], sen['receiver']
  ('chown', Pronoun, None, Addr: jim@example.org)

  >>> sen = parse('I yield Bob the Fortune Teller to <jim@example.org>.')[0]
  >>> sen['verb'], sen['subject'], sen['object'], sen['receiver']
  ('chown', Pronoun, 'bob the fortune teller', Addr: jim@example.org)

  >>> sen = parse('jim@example.org yields Bob the Fortune Teller to me.')[0]
  >>> sen['verb'], sen['subject'], sen['object'], sen['receiver']
  ('chown', Addr: jim@example.org, 'bob the fortune teller', Pronoun)

Activating/deactivating a character (from the timer/choreography)::

  >>> sen = parse('I am inactive.')[0]
  >>> sen['subject'], sen['verb']
  (Pronoun, 'deactivate')

  >>> sen = parse('Active.')[0]
  >>> sen['subject'], sen['verb']
  (None, 'activate')

  >>> sen = parse('Bob is active.')[0]
  >>> sen['subject'], sen['verb']
  ('bob', 'activate')

Errata
======

As phrase::

  >>> sen = parse('As Bob Johnson, ready.')[0]
  >>> sen['as']
  'bob johnson'

  >>> sen = parse('As for john@example.com, ready.')[0]
  >>> sen['as']
  Addr: john@example.com

  >>> sen = parse('For Tommy the Awesome Superhero, ready.')[0]
  >>> sen['as']
  'tommy the awesome superhero'

Multiple sentences::

  >>> sens = parse('I ready. I hold. I interrupt.')
  >>> [sen['value'] for sen in sens]
  ['ready', 'hold', 'interrupt']
