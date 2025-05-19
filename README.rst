PySQL
======

Introduction
-------------

|Github Stars| |Github Forks| |Github Open Issues| |Github Open PRs|

**PySQL** is an an object-relational mapper (ORM) for SQL databases,
written in Python. This library is designed to be lightweight,
easy to use and have zero-dependencies. The target audience is
anyone who wants a lighter alternative to `SQLAlchemy`_.

.. contents:: Table of Contents


Technologies Used
------------------

- Windows 10 x64
- Visual Studio Code
- Python 3.10


Project Status
---------------

This project is currently **in development**.


Version Naming
---------------

This library uses *semantic versioning*:

.. code:: txt

  MAJOR.MINOR.PATCH

Where an increment in:

- ``MAJOR`` = Incompatible changes (may require code to be updated).
- ``MINOR`` = Backwards compatible feature changes.
- ``PATCH`` = Backwards compatible bug fixes.


Getting Started
----------------

Let's create a simple sample program to display some of the core
features of this library.

- Clone the repository and ``pip install .`` in the root directory of
  the project.

.. code:: bash

  git clone "https://github.com/nicdgonzalez/PySQL.git"
  cd "./PySQL"
  pip install "."

- Create a new file and ``import`` the *pysql* package.

.. code:: python

  import pysql

- To connect to a database, ``import`` the target *connect* function
  from the target database's package, then pass it as an argument to
  the ``pysql.Database`` class. The library is designed this way so
  the client can install this package as a simple extension. No need
  to complicate things with additional dependencies you might never
  end up using.

.. code:: python

  # Connecting to a Database
  import sqlite3

  db = pysql.Database(
      sqlite3.connect,  # Positional-only argument.
      schema_name=None,  # Optional schema_name to use.
      # Any additional keyword arguments are passed to the connect function.
      datebase="pysql_demo.db"
  )

- For convenience, there is also a ``dict`` to URI converter class
  available:

.. code:: python

  import psycopg2
  from pysql import DatabaseURI

  config = {
      "engine": "postgres",
      "username": "postgres",
      "password": "secret",
      "host": "127.0.0.1",
      "port": "5000",
      "database": "postgres",
      "sslmode": "prefer",
      "timeout": 10.0
  }

  uri = str(DatabaseURI(**config))
  # or
  uri = DatabaseURI(**config).uri

  db = pysql.Database(
      psycopg2.connect,
      schema_name="postgres",
      dsn=uri
  )

- The default ``placeholder`` symbol for prepared statements is ``%s``.
  It may differ depending on which database engine you are using.
  For example, *sqlite3* uses ``?``. To change the placeholder symbol
  in this library, use the ``placeholder`` attribute on the ``Database``
  class:

.. code:: python

  db.placeholder = "?"

- To create a "Model", subclass the ``Model`` attribute from
  the ``Database`` class, then call the ``.create`` method.

.. code:: python

  class Prefixes(db.Model, name="prefixes"):
      guild_id = Column(pysql.Int8, not_null=True, unique=True)
      prefix = Column(pysql.Text, not_null=True, default="$")


  Prefixes().create()

- To insert data into the database, use ``db.session.insert``.
  Create an entry using the class object with keywords
  representing the column names and values representing
  data to insert into the table. e.g.,

.. code:: python

  guild_id = 794611010890629131
  entry = Prefixes(
      guild_id=guild_id,
      prefix="$"
  )
  db.session.insert(entry)

- To update a row in the database use ``db.session.update``:

.. code:: python

  db.session.update(Prefixes(prefix="?"), filter={"guild_id": guild_id})

- To delete a row from the database use ``db.session.delete``:

.. code:: python

  db.session.delete(Prefixes(guild_id=guild_id))

- To execute queries, use the ``query`` attribute of the ``Database``
  class:

.. code:: python

  result = db.query.fetch_one(Prefixes(guild_id=guild_id), select=["prefix"])
  # There is also:
  db.query.fetch_many
  db.query.fetch_all

- For additional actions available, refer to the documented source files in
  found in `/pysql <./pysql>`_.


Contributing
-------------

Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

- `Fork <https://github.com/nicdgonzalez/PySQL/fork>`_ the repository
  and create a new branch:

.. code:: powershell

  git pull --set-upstream "https://github.com/[username]/[repository_name].git"
  git checkout -b "improve-feature"

- Make the appropriate changes and stage the modified files:

.. code:: powershell

  git add <file(s)>

- Commit changes:

.. code:: powershell

  git commit -m "Improve feature."

- Push to the new branch:

.. code:: powershell

  git push "origin" "improve-feature"

- Create a `Pull Request <https://github.com/nicdgonzalez/PySQL/pulls>`_.


Bug/Feature Request
--------------------

If you find a bug (program failed to run and/or gave undesired results)
or you just want to request a feature, kindly open a new issue
`here <https://github.com/nicdgonzalez/PySQL/issues>`_.


Room for Improvement
---------------------

Areas that could use improvement:

- There is (barely, if any) documentation throughout the project.
  This is on the top of the priority list now that the project is
  now usable.

Unimplemented features:

- Only basic table operations have been implemented. Additional
  features will be implemented as time goes on.


.. |Github Stars| image:: https://badgen.net/github/stars/nicdgonzalez/pysql
.. |Github Forks| image:: https://badgen.net/github/forks/nicdgonzalez/PySQL
.. |Github Open Issues| image:: https://badgen.net/github/open-issues/nicdgonzalez/PySQL
  :target: https://github.com/nicdgonzalez/Learning-Japanese/issues?q=is%3Aissue+is%3Aopen+
.. |Github Open PRs| image:: https://badgen.net/github/open-prs/nicdgonzalez/PySQL
  :target: https://github.com/nicdgonzalez/Learning-Japanese/pulls?q=is%3Apr+is%3Aopen+

.. _SQLAlchemy: https://github.com/sqlalchemy/sqlalchemy
