musite - A `MutopiaProject <http://www.mutopiaproject.org>`_ web site
rewrite in `Django <http://djangoproject.com>`_

.. image:: https://readthedocs.org/projects/mudev-documentation/badge/?version=latest
:target: http://mudev-documentation.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status


Synopsis
--------

This repository is for development of a Python-based clone of the
MutopiaProject website using Python. It looks similar to the existing
site because the templating engine uses the same CSS files and
Bootstrap as the existing site. Underneath the covers, however, it is
entirely different.

   - Dynamic page creation for easier maintenance.

   - The entire MutopiaProject catalogue is kept within a
     `PostgreSQL <https://www.postgresql.org/>`_
     database for easy maintenance and analysis.

   - Supports full-text-search.


Overview
--------

Building a site with Django is a matter of defining an object
relationship model (``ORM``) and developing the website using view
code and html templates.

In Django-speak,

  - The ``Project`` is *musite*

  - The main website ``app`` is *mutopia*

  - An auxilliary ``app``, *update*, is provided for maintaining the
    underlying database.

You will find top-level project code under ``musite`` but the meat of
the web implementation is in ``mutopia``. If you are not familiar with
Django, I recommend starting with ``mutopia/models.py`` while keeping
the `Django documentation <https://docs.djangoproject.com>`_ handy.

The project documentation is done using
`Sphinx <http://sphinx-doc.org/>`_ under the ``docs`` folder.


Development setup
-----------------

This project uses typical Python tools. Once you clone the repository
you will need to create the appropriate virtual environment. A
``Makefile`` is provided for various developer tasks once that is
done. To install all the required development tools, ::

   $ make requirements
