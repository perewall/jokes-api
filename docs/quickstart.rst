Quickstart
----------

..  note::

    Application requires Python>=3.6 and SQL database

Only the SQLite database was tested, but theoretically there should be no problems with other databases (MySQL/PostgreSQL/etc)

You can configure application via environment variables or ``.env``, more in :mod:`jokes_api.config` module


Env
===

..  code-block:: shell

    python3 -m venv env
    . env/bin/activate


..  code-block:: shell

    pip install -r requirements.txt


Setup
=====

..  code-block:: shell

    python manage.py test


Configure database connection string (example):


..  code-block:: shell

    export JOKES_API_DATABASE_URL=sqlite:////tmp/jokes.db


Create database schema:


..  code-block:: shell

    python manage.py db upgrade


Create first user:


..  code-block:: shell

    python manage.py users create <username>


and remeber the user token, you will need it later


Start
=====

Run dev server:


..  code-block:: shell

    python manage.py run -h 127.0.0.1 -p 8000


and try to make request with ``curl``:


..  code-block:: shell

    curl -H "Authorization: <token>" localhost:8000/new


where ``<token>`` is token, which you got after user creation
