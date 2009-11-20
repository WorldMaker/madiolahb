===================
Character Ownership
===================

The Bee uses a very simple ownership model for characters. Each
character is owned by a single player. Ownership here is not for
security, but for pronoun usage and conceptual simplicity. Players can
force play for characters they do not own with the "as clause"
referencing another player's address: **[**\ As *player address*,...\
**]**.

  **[**\ As jim@example.com, Jim's Awesome Character readies.\ **]**

Character ownership can be transfered between players: **[**\ I yield
*Character name* to <*Player address*>.\ **]**. The triangular brackets
are required. This command is a rare exception to the Pronoun where it
always refers to "the current player".

  | **[**\ I yield the Bear to <jim@example.com>.\ **]**
  | **[**\ jim@example.com yields Jim's Awesome Character to me.\ **]**

================
Character Status
================

Characters by default are considered "active" and Bee tracks their
timing and presumes them eligible for upcoming turns. Characters can be
swapped between active and inactive status: **[**\ I am active.\ **]**
and **[**\ I am inactive.\ **]**.

.. vim: ai spell tw=72
