from uuid import uuid4

from flask_login import UserMixin, current_user
from requests import get as get_request

from . import db, auth


@auth.request_loader
def user_loader(request):
    token = request.headers.get('Authorization')

    if not token:
        return None

    try:
        return User.query.filter_by(token=token).first()
    except Exception:
        return None


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    username = db.Column(db.String(50), primary_key=True)
    token = db.Column(db.String(50), unique=True, default=f'{uuid4()}')

    jokes = db.relationship(
        'Joke', back_populates='user', cascade='all,delete')

    def __str__(self):
        return self.username


class Joke(db.Model):

    __tablename__ = 'jokes'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    user_id = db.Column(
        db.String(50), db.ForeignKey('users.username'), nullable=False)

    user = db.relationship('User', back_populates='jokes')

    def __str__(self):
        return f'id={self.id}, "{self.text}"'

    @property
    def as_dict(self):
        return dict(id=self.id, text=self.text)

    @classmethod
    def is_unique(cls, text):
        return not cls.query.filter_by(text=text, user=current_user).first()

    @classmethod
    def new(cls, url, timeout=5):
        response = get_request(url, timeout=timeout)
        response.raise_for_status()
        text = response.json()

        if not cls.is_unique(text):
            return cls.new(url, timeout)  # someday jokes will end

        return cls(text=text, user=current_user)
