Making updates
==============

.. include:: ../subs.txt

Overview
--------

There are several parts to the update process,

  - Building the assets from the contribution.
  - Pushing the assets to the data server.
  - Updating the database so the new piece is available on the site.

This document focuses on the final step, updating the database. There
is more information in the **mupub** project documentation on
:ref:`Publication <mupub:publication>`.


A note on Instruments
~~~~~~~~~~~~~~~~~~~~~

``Instrument`` objects take a little work to associate with a
``Piece`` because we have a contributor-written instrument list and a
well-defined list of instruments in the ``Instrument`` table. Most of
the issues are with plurals, idioms, and language,

  * plurals: 'two pianos' should form a single association to 'Piano'.
  * idioms: 'Uke' is not a known instrument but 'Ukulele' is.
  * language: 'Guitarre' needs to be translated to 'Guitar'

This leads to such a large number of misses it was decided to define
a database table for associating misses with actual instruments: the
``InstrumentMap``.

Each instance of an ``update.InstrumentMap`` contains a *candidate*
instrument name that can be associated with a known ``Instrument``
instance. When the RDF is read, the RDF field named *for* is read
directly into the ``Piece.raw_instrument`` field so it can be
tokenized and scanned for any instrument relationships.


.. _db-updating:

Updating models
---------------
There are several models that are integral to the update process,

  - ``update.InstrumentMap`` is a mapping of names to actual
    ``Instrument`` instances, used to allow for nicknames.
    misspellings, plurals, and languages.
  - ``update.Marker`` maintains a timestamp of when the update was
    performed.

  - ``mutopia.AssetMap`` is used in the presentation domain to locate
     the physical publication assets in the archive (its *assets*) as
     well as playing a role in updating.


Here is the outline of how an update works,

  - Read the timestamp in an ``update.Marker``.

  - Using the `github-api <https://developer.github.com/v3/>`_, query a
    one-line log from the github repository of changes since this
    timestamp.

  - Parse each line to find new and changed assets.

  - For each changed asset, update its corresponding row in the
    ``AssetMap`` and zero out its ``Piece`` reference.

  - Update the ``Marker`` with the current timestamp.

  - For each ``AssetMap`` rows with a null ``Piece`` reference,

    * Use the asset map to create the RDF file name.
    * Parse the RDF file to create or update the corresponding ``Piece``.
    * Save the new piece.

Breaking up this process into two sections has advantages,

  - If you want a *do-over* you can modify the ``Marker`` models table
    (``update_marker``) and delete the last timestamp.

  - A piece can be forced to update by nulling out the ``AssetMap``
    ``Piece`` reference manually, then re-running the update process.


This update process is embodied in an application management command
called ``update.dbupdate``.


Collections
~~~~~~~~~~~

Collections can be specific to a composer (an opus) or sets of related
pieces (The Gimo Collection). Adding or modifying a collection is not
so complicated but it is done manually. As shown in the
:ref:`database class diagram <db-class-diagram>`, a ``Collection`` is
shown as optional to a ``Piece`` (0..n) and has an M:M relationship.

**Use-case:** I've transcribed Matteo Carcassi's Opus 1, *Trois
Sonatines* as 3 separate files and, after submission and publication,
it is possible to create a collection of this small opus. I will
come up with a unique tag name, title, and the integer part of the
piece identifiers for this collection

 - For a tag name I chose "carcassiopus1". Note that this is not seen
   by the user but may be used to identify a folder with extended
   information about the collection.
 - A title for the collection ("Carcassi Opus 1, Trois Sonatines")

There are a number of ways to get the related ``piece_id`` values that
make up the collection. One way is to select **Latest Additions** on
the home page to get a list of recent submissions. By hovering the
mouse over the entries you can visually parse the integer
``piece_id``. Since I have access to the database and it is simple to
do this query based on the date published (I knew they were recent)
using ``psql``. The following SQL gets the 5 most recent submissions, ::

  $ mutodb
  mutodb=> select piece_id,composer_id,opus,title
  mutodb->    from mutopia_piece
  mutodb->    order by date_published desc limit 5;
   piece_id | composer_id |    opus     |         title
  ----------+-------------+-------------+------------------------
       2169 | CarcassiM   | Op. 1 No. 2 | Trois Sonatines, No. 2
       2170 | CarcassiM   | Op. 1 No. 3 | Trois Sonatines, No. 3
       2165 | CarcassiM   | Op. 1 No. 1 | Trois Sonatines, No. 1
       2168 | ChopinFF    | Op 28, No 9 | Prélude 9
       2166 | ChopinFF    | Op 28, No 8 | Prélude 8
  (5 rows)

Now we can use the website admin page to create the new collection.

 - Login into the admin.
 - Under **Mutopia** select ``+ Add`` on the line for **Collections**
 - Enter the tag and title.
 - In **Pieces:** , enter the ``piece_id`` values separated by commas
   in the order you want the pieces to appear. This allows you to
   "fix" situations where pieces are published out of order.
 - Select **Save**
 - View and review on the site. Edits can be made if necessary.
