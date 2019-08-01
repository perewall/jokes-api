from uuid import uuid4

from flask.cli import FlaskGroup
from click import group, argument, echo, ClickException

from . import create_app, db
from .models import User


@group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Jokes API"""


@cli.group('users')
def users_cli():
    """Jokes API users management"""


@users_cli.command('show')
def user_show():
    """Show users"""
    for user in User.query.all():
        echo(f'{user.username} {user.token}')


@users_cli.command('create')
@argument('username', nargs=1)
def user_create(username):
    """Create new user, returns user token"""
    if User.query.get(username):
        raise ClickException(f'User "{username}" already exist')

    user = User(username=username)
    db.session.add(user)
    db.session.commit()

    echo(f'User "{username}" successfully created, token: {user.token}')


@users_cli.command('delete')
@argument('username', nargs=1)
def user_delete(username):
    """Delete user by username"""
    user = User.query.get(username)

    if not user:
        raise ClickException(f'User "{username}" not found')

    db.session.delete(user)
    db.session.commit()

    echo(f'User "{username}" successfully deleted')


@users_cli.command('reset')
@argument('username', nargs=1)
def user_reset(username):
    """Generate new user token"""
    user = User.query.get(username)

    if not user:
        raise ClickException(f'User "{username}" not found')

    user.token = f'{uuid4()}'

    db.session.add(user)
    db.session.commit()

    echo(f'New user token: {user.token}')
