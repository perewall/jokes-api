from flask import Blueprint, current_app, request, jsonify, abort
from flask_login import login_required, current_user
from werkzeug.exceptions import HTTPException

from .models import db, Joke


views = Blueprint('views', __name__)


@views.app_errorhandler(Exception)
def jsonify_error(e):
    if isinstance(e, HTTPException):
        return jsonify(code=e.code, error=e.name, info=e.description), e.code
    current_app.logger.exception(f'Unhandled error: {e}')
    return jsonify(code=500, error='Internal', info='Fail'), 500


@views.route('/jokes', methods=['GET'])
@login_required
def my_jokes():
    """
    Get jokes list

    .. :quickref: jokes; Get jokes list

    **Request**:

        .. sourcecode:: http

            GET /jokes HTTP/1.1
            Authorization: <user-token-here>

    **Response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    "id": 1,
                    "text": "joke text here"
                },
                {
                    "id": 2,
                    "text": "another joke text here"
                }
            ]

    :reqheader Authorization: user token

    :statuscode 200: success
    :statuscode 401: invalid user token or *Authorization* header
    :statuscode 500: unexpected errors
    """
    return jsonify([joke.as_dict for joke in current_user.jokes])


@views.route('/new', methods=['GET'])
@login_required
def new_joke():
    """
    Generate new joke

    .. :quickref: jokes; Generate new joke

    **Request**:

        .. sourcecode:: http

            GET /new HTTP/1.1
            Authorization: <user-token-here>

    **Response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Content-Type: application/json

            {
                "id": 1,
                "text": "joke text here"
            }

    :reqheader Authorization: user token

    :statuscode 201: success
    :statuscode 401: invalid user token or *Authorization* header
    :statuscode 500: unexpected errors
    :statuscode 503: jokes provider errors
    """
    try:
        joke = Joke.new(current_app.config['JOKES_PROVIDER_URL'])
    except Exception as e:
        current_app.logger.exception(f'Bad joke: {e}')
        return abort(503, 'Bad joke')
    else:
        db.session.add(joke)
        db.session.commit()
        current_app.logger.info(f'Make new joke {joke}')
        return jsonify(joke.as_dict), 201


@views.route('/<int:joke_id>', methods=['GET'])
@login_required
def get_joke(joke_id):
    """
    Get joke by id

    .. :quickref: jokes; Get joke by id

    **Request**:

        .. sourcecode:: http

            GET /1 HTTP/1.1
            Authorization: <user-token-here>

    **Response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "id": 1,
                "text": "joke text here"
            }

    :reqheader Authorization: user token

    :statuscode 200: success
    :statuscode 401: invalid user token or *Authorization* header
    :statuscode 404: joke not found or owned by another user
    :statuscode 500: unexpected errors
    """
    joke = Joke.query.filter_by(id=joke_id, user=current_user).first_or_404()
    current_app.logger.info(f'Get joke {joke}')
    return jsonify(joke.as_dict)


@views.route('/<int:joke_id>', methods=['PUT'])
@login_required
def update_joke(joke_id):
    """
    Update joke text by id

    .. :quickref: jokes; Update joke text

    **Request**:

        .. sourcecode:: http

            PUT /1 HTTP/1.1
            Authorization: <user-token-here>
            Content-Type: application/json

            {"new joke text"}

    **Response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "id": 1,
                "text": "new joke text"
            }

    :reqheader Authorization: user token
    :reqheader Content-Type: application/json

    :statuscode 200: success
    :statuscode 400: invalid request body or *Content-Type* header
    :statuscode 401: invalid user token or *Authorization* header
    :statuscode 404: joke not found or owned by another user
    :statuscode 409: joke with the same text is already exist
    :statuscode 500: unexpected errors
    """
    joke = Joke.query.filter_by(id=joke_id, user=current_user).first_or_404()

    text = request.get_json()
    if not text:
        return abort(400, 'Joke text is not provided')

    if not Joke.is_unique(text):
        return abort(409, 'Joke text must be unique')

    joke.text = str(text)

    db.session.add(joke)
    db.session.commit()

    current_app.logger.info(f'Update joke {joke}')
    return jsonify(joke.as_dict)


@views.route('/<int:joke_id>', methods=['DELETE'])
@login_required
def delete_joke(joke_id):
    """
    Delete joke by id

    .. :quickref: jokes; Delete joke by id

    **Request**:

        .. sourcecode:: http

            DELETE /1 HTTP/1.1
            Authorization: <user-token-here>

    **Response**:

        .. sourcecode:: http

            HTTP/1.1 204 NO CONTENT

    :reqheader Authorization: user token

    :statuscode 204: success
    :statuscode 401: invalid user token or *Authorization* header
    :statuscode 404: joke not found or owned by another user
    :statuscode 500: unexpected errors
    """
    joke = Joke.query.filter_by(id=joke_id, user=current_user).first_or_404()

    db.session.delete(joke)
    db.session.commit()

    current_app.logger.info(f'Delete joke {joke}')
    return '', 204
