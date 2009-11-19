===========================
Dealing with the Time Track
===========================

As a choreographer for the HCE, the time track is obviously considered
the primary domain for the Bee.

.. contents::

Ready and Hold
==============

The Bee will announce which character or characters it thinks are
eligible at the current tick. A character can reply with **[**\ I am
ready.\ **]** to take a turn or **[**\ I hold.\ **]** to wait or pass.

Interrupting
============

A character can force a turn when the Bee thinks they are ineligible
with **[**\ I interrupt.\ **]**. The need to use this should be rare.

Setting the Time Track
======================

A character's turn ends when the character sets their own timer, **[**\
I set myself to *Time Count*.\ **]** where *Time Count* is 0, 1, 2, 3,
4, 5, 6, or 9. If the Bee remembers your last action (ie, it happens to
be in the current email message or Wave blit), you can omit the **[**\
...to *Time Count*.\ **]** and the Bee will set the character to the
used influence's count. If the Bee remembers the dice roll of that
action, it will double check the intended timing effect against your
time track setting.

A character can also set another character's time track with **[**\ I
set *Character Name* to *Time Count*.\ **]**. This allows the Bee to
double-check the entire timing effect against a dice roll, given that
Bee remembers the dice roll.

The parser accepts the verb "reset" as a synonym of "set".

.. vim: ai spell tw=72
