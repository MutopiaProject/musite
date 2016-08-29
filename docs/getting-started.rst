Getting Started
===============

.. include:: subs.txt

For developers, this documents the tools required for contributions
and outlines the installation on the platform I use (Ubuntu 16.04).
The project should travel well to other environments.

The project uses |heroku| to demo the site. More on that later.


.. _requirements:

Requirements
------------

The following tools are necessary to get started:

 - **python3**
 - **virtualenv** and **virtualenvwrapper**
 - **PostgreSQL**, this was developed using version 9.4

Virtual environments provide a mechanism of library definitions so
that developers on different platforms can match environments.

.. _installing:

Installing the Basic Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Start by setting up for virtual environments. ::

  $ sudo apt-get virtualenv,virtualenvwrapper

Virtual environments will allow us to match environments among
developers. To create one for this project that will use ``python3``
exclusively, ::

  $ mkvirtualenv --python=python3 musite

More conveniently, if you have cloned the workspace into a folder
called ``$HOME/work/musite``, you can associate that folder with the
environment so that using the environment will also set your working
folder, ::

  $ mkvirtualenv --python=python3 musite $HOME/work/musite

Once in this environment we can install the other required tools.
Moving among environments is done with the ``workon`` tool, ::

  $ workon musite
  (musite) $ python --version
  Python 3.5.2

Among other things, the virtual environment will also install pip
which will allow you to install specific versions of packages from a
file. The requirements have been separated into several files,

 - **common.txt** - libraries required for both production and
   development.

 - **development.txt** - developer libraries; includes tools like
   coverage, pylint, and sphinx.

 - **production.txt** - production only

These are simple text files that specify the version of each tool you
need. As an example, for development you would include the ``common``
and ``development`` requirements ::

  (musite) $ pip install -r requirements/common.txt
  (musite) $ pip install -r requirements/development.txt

The development environment will also install the documentation tool,
|sphinx|. (Hey, just trying to help, here!) There is a ``Makefile``
supplied for developers so you can simply do this, ::

  (musite) $ make requirements

You may have as many environments as you like but take care to work on
the correct environment when you develop code in this project.


.. _env-var-label:

Environment Variables
---------------------

The few environment variables necessary for working with this project
have to do with running a local |django| test server. They are,

    **MU_CONFIG** [default: 'PRODUCTION']
        Valid values are 'DEVELOPMENT', 'STAGING', or 'PRODUCTION'.
        The default is PRODUCTION so we don't accidentally ship a
        development product. During development the site has fewer
        security features and has |django|'s DEBUG flag enabled.

    **MU_SECRET_KEY** [default: None]
        This is supplied and inserted into the |django| settings file
        when the project is created. The problem is that we don't
        really want it to be there and the typical strategy is to move
        it to an environment variable. You will need to get this value
        from the project manager.


.. _pg-configure-label:

Configuring PostgreSQL
----------------------

Here is a summary of the steps for install postgres on ubuntu, if you
get lost you can go to these `ubuntu pages <https://help.ubuntu.com/community/PostgreSQL/>`_. ::

  $ sudo apt-get install postgresql postgresql-contrib

During installation, the system should have created a postgres user
that you will need for defining system-wide postgres configuration. It
should have a password and, just so the usage can be shown, here is how you
would change the password, ::

  $ sudo -u postgres psql postgres
  postgres=# \password
  postgres=# \q

To break that down,

* `sudo -u postgres` - runs a command as user postgres
* `psql postgres` - run the ``postgres`` command-line using the
  postgres database (which is where the configuration tables live.)
* `\\password` is a command to the interpreter to change your password.
  It will prompt for the new password.
* `\\q` quits the interpreter


Full Text Search
----------------

FTS is available by default in postgres but the
normalization of accented characters is an extension that, while built
in, needs to be enabled in order to work. The extension is called
*unaccent* and it can be enabled by creating an extension on the
database. In the following command it creates the extension on a
database called *template1* which sets up *unaccent* on the
default database template, ::

  $ sudo -u postgres psql -d template1 -c 'create extension unaccent;'

Note that when you make changes to the |postgres| database, as
above, you are actually modifying the default database configuration
for all users. You want to do this in the event you write tests that
use this extension.

.. _pg-django-label:


The Database for Django
~~~~~~~~~~~~~~~~~~~~~~~

The default database for a |django| project
is SQLite, which is convenient since it requires no extra
configuration. In that mode, |django| will do all the work of creating
the database and its tables without much grief from the user. To have
FTS we need to switch the database back-end to |postgres| and that
means extra configuration is required. Here are the steps, ::

  $ sudo -u postgres createdb mutopiadb
  $ sudo -u postgres psql
  CREATE ROLE muuser WITH LOGIN PASSWORD 'mumusic';
  GRANT ALL PRIVILEGES ON DATABASE mutopiadb TO muuser;
  ALTER USER muuser CREATEDB;

The ``createdb`` used in the first line is a utility provided by the
``postgresql`` installation. The next few steps use the |psql| utility
to create a user (*muuser*) with a password. These can be changed but
must match those found in the |django| settings file. We give our user
all privileges on the database and, lastly, we let our user create
databases so the application tests can create and delete a temporary
database.

At this point you have an empty database. The first step is to have
|django| create all the tables defined by the models. This is all done
using ``manage.py`` in the ``musite`` environment. It looks like a lot
of work but you only have to do this once for an empty database, ::

  (musite) $ # first off, the django apps
  (musite) $ python manage.py migrate
  (musite) $ # now our apps, mutopia and update
  (musite) $ python manage.py makemigrations mutopia
  (musite) $ python manage.py migrate mutopia
  (musite) $ python manage.py makemigrations update
  (musite) $ python manage.py migrate update

Now you have all the tables defined but no data. If you ran a local
web server (``manage.py runserver``) you would get a fairly lame web
site but at least you would get one. Populating the database is
covered in :doc:`db/howto`.

For those not familiar with |django|, the migration process allows for
changes in the model. If you decide to add an attribute to an existing
model, you need to have |django| make a migration for it. The column
is added when you migrate the app. You may have to manually populate
this column. [#f1]_

.. _django-notes-label:

Notes on Django
~~~~~~~~~~~~~~~

.. rubric:: Static files

If you tried running a local server and got plain HTML output and no
graphics, you will need to collect the static files into a working
folder for the local server, ::

  (musite) $ python manage.py collectstatic

This moves all the project and application graphics and CSS from
various locations and gets them all into a place known by the
server. A production server may use a more distributed layout but
that's taken care of in the |django| settings.

.. rubric:: Django settings

When a |django| project is started, their admin scripts provide a
default structure with enough content to allow you to start working
immediately. The default database is *sqlite* because it is
generally available and requires little configuration.

There are several problems to solve in the ``musite.settings``
module,

 - using |heroku| for the site demos (Staging).
 - using a local server and database for simulation and
   testing (Development).

A |django| extension called ``dj-configurations`` is used to provide
an environment for both Production and Development using a single
settings file (see :ref:`pg-configure-label`).

.. rubric:: Footnotes

.. [#f1] There are complexities in data migration that can't be
         covered in this document. The migration mechanism makes a
         complex task relatively easy so it shouldn't be feared.
