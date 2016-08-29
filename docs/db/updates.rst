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


Updating FTS
~~~~~~~~~~~~
Because free text search is implemented as a *materialized view* it
can be recreated or refreshed at any time but does not have its own
fixture. An additional management command, ``postgres_fts`` is
provided to create the view from scratch or refresh it. ::

  (musite) $ python manage.py postgres_fts
  (musite) $ python manage.py postgres_fts --refresh
