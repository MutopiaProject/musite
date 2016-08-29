Database How-to
===============

.. include:: ../subs.txt

Before getting here you should have read,

 - :ref:`pg-configure-label`
 - :ref:`pg-django-label`

This section covers basic database details like :ref:`db-populating`
and :ref:`db-updating` and assumes you have |django| configured and
your database has been created but not yet populated.

If you are more interested in database design before going through
this chapter, see :doc:`design`.

.. _db-introduction:

Introduction
------------

The |mutopia| website is a read-only interface to an archive of
musical pieces. Our project has two essential goals,

 - Present the current archive as a website.
 - Be aware of newly submitted pieces that have been added to the
   archive but are not yet shown on the site.

These are embodied by two |django| apps,

 - ``mutopia`` is the website itself
 - ``update`` for scanning the archive for new pieces and adding them
   to the database.

This document is concerned with understanding a little bit about how
|django| can take care of some of the maintenance tasks of the
database.

.. rubric:: Models and tables

|django| provides a framework to define tables and their relationships
using python code. Once you have defined models as specified by
|django|, creating and modifying instances of those models will modify
the underlying tables in the database. We may use the term *model* and
*table* interchangeably since there is always a one-to-one
correspondence of a model to its table.


.. _db-populating:

Populating the database
-----------------------
|django| uses `JSON <https://en.wikipedia.org/wiki/JSON>`_ for its
database output format. Without going into why this is a good idea,
let's take a look at the methods for backing up and restoring. These
two commands will output the Composer model and then load it back in, ::

  (musite) $ python manage.py dumpdata \
      --indent=2 \
      --output=composer.json mutopia.Composer
  (musite) $ python manage.py loaddata comp.json

The ``indent`` option makes the output more readable and is
unnecessary if you don't plan to read them. Within |django| this JSON
output is called a fixture.

A number of fixtures are provided for those parts of the model that
have no dependencies. These are best explained by a script, ::

  LOAD="python manage.py loaddata"
  MUTOPIA_MODELS="                                \
    Composer                                      \
    Contributor                                   \
    Style                                         \
    Instrument                                    \
    LPVersion                                     \
    License"

  for t in $MUTOPIA_MODELS; do
      $LOAD mutopia/fixtures/${t}.json
  done

If you are familiar with how the original archive structure was
updated, some of these will be familiar to you. The detail of these
are not described here, they are each outlined in
:doc:`../modules/mutopia`.

The fixtures that are missing above are the **big** ones,

  - ``Piece``, the actual contributed piece.
  - ``AssetMap``, a mapping of the piece to its physical assets on a
    storage server somewhere.
  - ``Collection``, not so big but needs ``Piece`` to be defined first.
     
These fixtures should be provided in a zip file for developers.
