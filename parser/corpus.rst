Language Corpus
===============

:Copyright: 2009 Max Battcher. Some Rights Reserved (CC by-sa).

This is a collection of doctests to test that sentences in the language
parse as expected.

IM State Management
-------------------

The IM state sentences to define games::

  >>> sen = parse('This is called the test game.')[0]
  >>> print sen['imsentence'], sen['name'], sen['verb']
  True the test game is

  >>> sen = parse('Thus continues the test game.')[0]
  >>> print sen['imsentence'], sen['name'], sen['verb']
  True the test game continues

  >>> sen = parse('This ends the test game.')[0]
  >>> print sen['imsentence'], sen['name'], sen['verb']
  True the test game ends

Double check that other sentences are not IM sentences::

  >>> parse('Ready.')[0]['imsentence']
  False

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
  >>> sen['verb'], sen[1]
  ('advanced', 3)

  >>> sen = parse('I advanced 3 in my first profession.')[0]
  >>> sen['verb'], sen[1]
  ('advanced', 3)

  >>> sen = parse('I advanced 2 in profession 2, 3 in profession 1, and 1 in my third profession.')[0]
  >>> sen['verb'], sen[1], sen[2], sen[3]
  ('advanced', 3, 2, 1)

  >>> sen = parse('Advanced 3 in my first profession.')[0]
  >>> sen['verb'], sen[1]
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

Game Flow
---------

Timing verbs::

  >>> sen = parse('Ready.')[0]
  >>> sen['subject'], sen['verb']
  (None, 'ready')

  >>> sen = parse('I ready.')[0]
  >>> sen['subject'], sen['verb']
  (Pronoun, 'ready')

  >>> sen = parse('He readies.')[0]
  >>> sen['subject'], sen['verb']
  (Pronoun, 'readies')

  >>> sen = parse('I hold.')[0]
  >>> sen['subject'], sen['verb']
  (Pronoun, 'hold')

  >>> sen = parse('I interrupt.')[0]
  >>> sen['subject'], sen['verb']
  (Pronoun, 'interrupt')

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

  >>> sen = parse('He heroically acts with mastery.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('act', 'mastery', True, 0)

  >>> sen = parse('I act with charm under my first profession.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('act', 'charm', False, 1)

  >>> sen = parse('Act with design.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('act', 'design', False, 0)

  >>> sen = parse('Heroic action in sleight.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('act', 'sleight', True, 0)

Challenged actions::

  >>> sen = parse('I challenge Bob in poise.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('contest', 'poise', False, 0)
  >>> sen['object']
  'bob'

  >>> sen = parse('He heroically challenges him with mastery.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('contest', 'mastery', True, 0)
  >>> sen['object']
  Pronoun

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

  >>> sen = parse('Heroically challenge the Pope in sleight.')[0]
  >>> sen['verb'], sen['influence'], sen['heroic'], sen['profession']
  ('contest', 'sleight', True, 0)
  >>> sen['object']
  'the pope'

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

Setting the Time
----------------

Resetting and otherwise setting the time track::

  >>> sen = parse('Reset.')[0]
  >>> print sen['verb'], sen['time'], sen['object']
  set None None

  >>> sen = parse('Set to 1.')[0]
  >>> print sen['verb'], sen['time'], sen['object']
  set 1 None

  >>> sen = parse('Set myself to 1.')[0]
  >>> print sen['verb'], sen['time'], sen['object']
  set 1 Pronoun

  >>> sen = parse('Reset myself.')[0]
  >>> print sen['verb'], sen['time'], sen['object']
  set None Pronoun

Errata
======

As phrase::

  >>> sen = parse('As Bob Johnson, ready.')[0]
  >>> sen['as']
  'bob johnson'

  >>> sen = parse('As for john@example.com, ready.')[0]
  >>> sen['as']
  Addr: john@example.com

  >>> sen = parse('For Jason the Awesome Superhero, ready.')[0]
  >>> sen['as']
  'jason the awesome superhero'

Multiple sentences::

  >>> sens = parse('I ready. I hold. I interrupt.')
  >>> [sen['verb'] for sen in sens]
  ['ready', 'hold', 'interrupt']
