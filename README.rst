.. image:: https://travis-ci.com/perewall/jokes-api.svg?branch=master
    :target: https://travis-ci.com/perewall/jokes-api

.. image:: https://codecov.io/gh/perewall/jokes-api/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/perewall/jokes-api


Jokes API
=========

Multi user REST API for jokes management and generation (via `public api`_)

This application is a test task, written on Python with Flask_

.. _Flask: http://flask.pocoo.org/
.. _`public api`: https://geek-jokes.sameerkumar.website/api



Setup
-----

    Application requires Python>=3.6
    and SQL database (SQLite/MySQL/PostgreSQL/etc)

Create virtual environment:

..  code-block:: shell

    python3 -m venv env
    . env/bin/activate


Install requirements:

..  code-block:: shell

    pip install -r requirements.txt


Run unit tests:

..  code-block:: shell

    python manage.py test


Configure database connection string via environment variable or ``.env``:

..  code-block:: shell

    export JOKES_API_DATABASE_URL=sqlite:////tmp/jokes.db


Create database schema:

..  code-block:: shell

    python manage.py db upgrade


Create first user:

..  code-block:: shell

    python manage.py users create <username>

and remeber the user token, you will need it later



Usage
-----

..  code-block:: shell

    python manage.py --help


Run dev server:

..  code-block:: shell

    python manage.py run -h 127.0.0.1 -p 8000


and try to make request with ``curl``:

..  code-block:: shell

    curl -H "Authorization: <token>" localhost:8000/new

where ``<token>`` is token, which you got after user creation



Documentation
-------------

Usage examples and API description

Build docs with Sphinx_:

..  code-block:: shell

    python manage.py docs -o htmldoc

and open ``htmldoc/index.html`` in your favourite browser

.. _Sphinx: http://www.sphinx-doc.org
