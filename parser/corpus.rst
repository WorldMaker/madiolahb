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
  >>> sen['verb'], sen['profs'][0]
  ('advanced', (1, 3))

  >>> sen = parse('I advanced 3 in my first profession.')[0]
  >>> sen['verb'], sen['profs'][0]
  ('advanced', (1, 3))

  >>> sen = parse('I advanced 2 in profession 2, 3 in profession 1, and 1 in my third profession.')[0]
  >>> profs = dict(sen['profs'])
  >>> sen['verb'], profs[1], profs[2], profs[3]
  ('advanced', 3, 2, 1)

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
  >>> print sen['subject'], sen['verb']
  None ready

  >>> sen = parse('I ready.')[0]
  >>> print sen['subject'], sen['verb']
  Pronoun ready

  >>> sen = parse('He readies.')[0]
  >>> print sen['subject'], sen['verb']
  Pronoun readies

  >>> sen = parse('I hold.')[0]
  >>> print sen['subject'], sen['verb']
  Pronoun hold

  >>> sen = parse('I interrupt.')[0]
  >>> print sen['subject'], sen['verb']
  Pronoun interrupt

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
