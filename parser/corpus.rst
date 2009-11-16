Language Corpus
===============

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
  >>> print sen['verb'], sen['time'], sen['subject']
  set None None

  >>> sen = parse('Set to 1.')[0]
  >>> print sen['verb'], sen['time'], sen['subject']
  set 1 None

  >>> sen = parse('Set myself to 1.')[0]
  >>> print sen['verb'], sen['time'], sen['subject']
  set 1 Pronoun

  >>> sen = parse('Reset myself.')[0]
  >>> print sen['verb'], sen['time'], sen['subject']
  set None Pronoun
