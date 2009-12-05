======
Acting
======

The key part of a character's turn involves deciding upon an influence,
a type of action, exerting any will necessary for the action, and if
necessary rolling to determine the Fate of the action.

.. contents::

Exerting Will
=============

A character can exert will, moving will from the source to the
influence, by **[**\ I exert *Number* to *Influence*.\ **]**. Multiple
"count to influences" can be chained in a single sentence, with optional
comma and/or "and", should this be needed.

The word "flow" can also be substituted as a synonym of "exert".

  **[**\ I exert 2 to poise.\ **]**

Starting an action
==================

The choices to be made in setting up an action:

* The influence in question

* Contested versus uncontested --- This is represented by the verb
  choice: "contest" or "challenge" versus "act"

* Heroic versus mundane --- The words "hero", "heroic", or "heroically"
  can be used as an adverb to signal a heroic action, whereas mundane is
  the default

* For a contested action a character needs to be chosen to be challenged

* Whether an action qualifies as a professional action --- An "under
  clause" can be appended to choose a profession: **[**\ ...under
  profession *Number*.\ **]** or **[**\ ...under my *Cardinal number*
  profession.\ **]**

Thus the four major forms of the action command:

  | **[**\ I act with *Influence*.\ **]**
  | **[**\ I heroically act with *Influence*.\ **]**
  | **[**\ I challenge *Character name* with *Influence*.\ **]**
  | **[**\ I challenge *Character name* heroically with *Influence*.\
    **]**

An example:

  **[**\ I heroically contest The Bear with charm under my first
  profession.\ **]**

Based upon this information, and will exerted, the Bee will determine if
a roll needs to be made and if so will report the roll's success.

Losing ego
==========

Sometimes fate conspires to cause character's to lose ego. **[**\ I lose
*count* ego.\ **]** If Bee remembers the last roll it will helpfully
double-check your math here.

  **[**\ I lose 2 ego.\ **]**

Recovering spent ego and will
=============================

Given a skein defined system for healing or resting, a character can
recover spent ego and will with **[**\ I recover *count* ego.\ **]**.
"Will" can be substituted for ego. If neither "will" nor "ego" is
provided, the Bee will try first recovering will and then recovering
ego. Additionally, the count and the type can both be omitted and the
Bee will recover the default flow amount from first will and then ego.

  | **[**\ I recover 3 ego.\ **]**
  | **[**\ I recover 2 will.\ **]**
  | **[**\ I recover 4.\ **]**
  | **[**\ I recover.\ **]**

Moving
======

The Bee keeps track of a basic notion of a character's position using an
integer (x, y) coordinate system. The absolute position can be set with
the "at" verb: **[**\ I am at *X*, *Y*.\ **]** where *X* and *Y* are
integers. Whereas relative position changes can be commanded by "move":
**[**\ I move *Character* to *Count* spots *Direction*.\ **]** The
object of the move can be omitted, as with the action verbs above.
Relative movement is compared by the Bee (as best as it can) to a
remembered roll.

Directions accepted are the abbreviations for everyone's favorite
compass directions (one of N, S, E, W, NE, NW, SE, or SW). Generally the
Bee assumes a hex map and the coordinate system should reflect that, for
instance E and W counts should be multiples of 2.

Synonyms for "spots" includes "spaces" and "paces". The word can also be
elided entirely.

.. todo::

   This will obviously be an under-powered support until actual maps can
   be presented... when it will probably warrant a section all to
   itself.

==============================
Example for a Character's Turn
==============================

Given that Bee has announced that a character has "ticked" to the ready
spot, the character can start a new turn and then proceed to exert will
and then announce an action.

  **[**\ I ready. I exert 1 to poise. I act with poise.\ **]**

Upon reading this command sequence the Bee should report the results of
a dice roll if it is necessary. In this case, the Bee should report a
guaranteed success of the mundane action, with an expected effect less
than or equal to 3 and timing less than or equal to 1. The player can
freely role play what the action was, in non-bracketed text.

  I rushed towards that vending machine...

Following all that warm roleplaying, let Bee know the effects of the
action, finishing with timing effect on the character itself.

  ...I can't wait to get that nice, cold Root Beer of Righteous
  Benevolence. **[**\ I move 1 spot NW. I reset to 2.\ **]** I do hope I
  have enough change.

.. vim: ai spell tw=72
