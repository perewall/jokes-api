Command-line interface
----------------------

Based on click_ library

.. _click: https://click.palletsprojects.com


Users management
================

You can add/remove users and refresh token with CLI **only**

The token obtained after creating the user is used in the ``Authorization``
header when accessing the API methods

..  code-block:: shell

    python manage.py users --help


..  code-block:: shell

    Usage: manage.py users [OPTIONS] COMMAND [ARGS]

      Jokes API users management

    Options:
      --help  Show this message and exit.

    Commands:
      create  Create new user, returns user token
      delete  Delete user by username
      reset   Generate new user token
      show    Show users
