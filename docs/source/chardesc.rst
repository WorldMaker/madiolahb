=====================
Describing Characters
=====================

Generally the first thing to do in a game will be to describe the
characters currently being played. These commands can (and may) be used
at any point in a game, but will often be primarily associated with
beginning a new game.

A note on terminology: the Bee refers to the objects that it manipulates
as characters and this documentation will refer to them as such, but
they don't necessarily have to be "characters". In HCE terms, anywhere
you see the word character you may mentally replace it with "thing with
a Life Wheel".

.. contents::

Creating a Character
====================

A character needs to be created before it can be played. **[**\
*Address* is playing *Character Name*.\ **]** where *Address* is the
player (IM address, email address, or Wave address) that will own (play)
that character. Keep in mind the character naming rules, and this
command will be your first and best place to learn if the Bee has any
problems with the name you chose.

  | **[**\ jim@example.com is playing Tommy Jones.\ **]**
  | **[**\ I am playing Barnaby.\ **]**

This command is a rare exception to normal Pronoun handling: Because
this command deals specifically with a player rather than a character,
the Pronoun here represents "the current player". This command
automatically sets "the current character" to the newly created
character, for pronouns in subsequent commands.

Placing Tokens on the Life Wheel
================================

The "have verb" sets a number of tokens for a given spot on the life
wheel for a character. The basic forms look like:

  | **[**\ I have *Number* ego.\ **]**
  | **[**\ I have *Number* will.\ **]**
  | **[**\ I have *Number* *Element*.\ **]**
  | **[**\ I have *Number* ego drained.\ **]**
  | **[**\ I have *Number* will drained.\ **]**
  | **[**\ I have *Number* will spent.\ **]**

One or more of these can be combined, "have" will accept a list of forms
above, optionally separated by a comma and/or "and".

"Ego" and "will" refer to ego and will tokens in the source, while the
"drained" form refers to tokens in the ego and will spaces of the life
wheel. The drained forms should be rarely used in the event of resetting
a game or correcting a Bee mistake. "Dissipated" can be used as a
synonym of drained, and "spent" is used with will to denote will placed
upon the ego space on the life wheel.

  **[**\ I have 9 ego, 12 will, 3 life, and 3 energy.\ **]**

Advancing in a Profession
=========================

**[**\ I have advanced *Number* in profession *Number*.\ **]**
Professions are referred to by number (1, 2, or 3) and multiple
professions can be set in a single sentence, chaining them with an
optional comma and/or "and". Professions can also be referred by a
cardinal number ("first", "second", or "third") in the form **[**\ ...in
my *Cardinal* profession.\ **]**.

Although the verb here is "advanced" (or "have advanced"), the number
provided is the *absolute* number of tokens (and thus can in fact
represent a decrease in profession).

  **[**\ I have 3 in my first profession, 2 in profession 2, and 3 in my
  third profession.\ **]**

.. vim: ai spell tw=72
