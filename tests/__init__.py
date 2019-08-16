from os import environ
from unittest import TestCase

from responses import reset

from jokes_api import db, create_app
from jokes_api.models import User, Joke
from jokes_api.config import DefaultConfig


class TestConfig(DefaultConfig):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get(
        'JOKES_API_DATABASE_URL', 'sqlite://')


class TestApp(TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        self.app_context = self.app.test_request_context()
        self.app_context.push()

        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        reset()
        db.session.commit()
        db.drop_all()
        self.app_context.pop()

    def makeUser(self, username=None):
        user = User(username=username or 'fake')
        db.session.add(user)
        db.session.commit()

        return user

    def makeJoke(self, text=None, user=None):
        if not user:
            user = self.makeUser()

        joke = Joke(text=text or 'fake joke', user=user)
        db.session.add(joke)
        db.session.commit()

        return joke
