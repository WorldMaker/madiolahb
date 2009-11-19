======================
Command Language Guide
======================

This guide is intended as a rather complete guide and reference to all
of the commands the Bee will respond to. It shouldn't be necessary for
every storyteller in a game to know this document inside and out to
play. (For that purpose there are the Quick Reference guides.)

.. todo::

   Write the quick reference guides and link them here.

.. contents::

Overview
========

The Bee listens for commands surrounded in square brackets. The commands
that it expects are meant to appear like English sentences and should
generally follow the structure an English speaker would expect. Every
command ends with a period.

There are a few conventions used in this document, intended to keep the
language examples clear to follow. The square brackets around examples
will be **bold** to help examples stand out. Variables that can be replaced
will be *italicized*. Most examples will use rather verbose sentence
formations and a first-person format, but the Bee will parse several
more examples than specifically mentioned in this document. Example:

   **[**\ I move *Character Name* to *count* spaces *direction*.\ **]**

The parser also supports the obvious third-person variations of verbs
and many words in a sentence can be elided, including the subject for
a more imperative tone.

.. note::

   It may be important to keep in mind that although commands *look*
   like English, the parser is **stupid**.

Pronouns
========

One particular simplification to keep in mind when working with the Bee:
*there is only one pronoun*. While you can use all your favorite friends
to represent it (such as I, he, she, and it), the parser doesn't pay
attention to which particular one you used and using different English
pronouns in the same sentence doesn't affect the meaning to the Bee.

For players with one and only one character The Pronoun refers to "the
current player's character". Players with multiple characters will deal
with The Pronoun as "the current character". The current character is
implicitly set in most sentences. The current character can be set
*explicitly* with the "as clause", which can be prepended to most
commands:

  This example won't parse, as it needs a command, but should get the
  point across... **[**\ As *Character Name*, ...\ **]**

It is important to note that the comma ending the clause is
**required**. For role-playing purposes the synonyms "For" and "As for"
can also be used to begin the clause. The "as clause" sets the current
character for the duration of the current email message or Wave blit.
(The Bee will not remember beyond that.)

Character Naming Restrictions
=============================

Bee tries to be as flexible as possible in parsing character names,
which as the examples above alone show are used in many different ways,
but there are still some restrictions required to keep things sensible.
Hopefully the general overall flexibility provided makes up for the few
cases where you may bump into a syntax error.

* Names are case insensitive (as is the rest of the parser)
* Names may consist of any number of words
* Names **may not** contain any commas or periods
* Names may contain any other punctuation or unicode characters
* Names **may not** contain any reserved words

.. todo::

   Should probably create a nicely formatted list/table of all
   reserved word combinations... For now, people are welcome to consult
   the grammar itself.

Also, names are opaque strings to the Bee, so the character name needs
to be written in full each time it appears.

Commands
========

.. toctree::
   :maxdepth: 2

   chardesc
   timing
   acting

.. vim: ai spell tw=72
