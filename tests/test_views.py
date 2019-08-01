from flask import url_for
from responses import activate, add, replace

from jokes_api.models import Joke

from tests import TestApp


class TestView(TestApp):

    def test_view_jsonify_error(self):
        joke = self.makeJoke()
        url = url_for('views.my_jokes')
        headers = dict(Authorization=joke.user.token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(joke.as_dict, response.json)

    def test_view_my_jokes(self):
        joke = self.makeJoke()
        url = url_for('views.my_jokes')
        headers = dict(Authorization=joke.user.token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(joke.as_dict, response.json)

    @activate
    def test_view_new_joke(self):
        headers = dict(Authorization=self.makeUser().token)

        add('GET', self.app.config['JOKES_PROVIDER_URL'], json='new joke')
        response = self.client.get(url_for('views.new_joke'), headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['text'], 'new joke')

        replace('GET', self.app.config['JOKES_PROVIDER_URL'], json=None)
        response = self.client.get(url_for('views.new_joke'), headers=headers)
        self.assertTrue(response.status_code >= 500)

    def test_view_get_joke(self):
        joke = self.makeJoke()
        url = url_for('views.get_joke', joke_id=joke.id)
        headers = dict(Authorization=joke.user.token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(joke.as_dict, response.json)

    def test_view_update_joke(self):
        joke = self.makeJoke()
        url = url_for('views.update_joke', joke_id=joke.id)
        headers = dict(Authorization=joke.user.token)

        response = self.client.put(url)
        self.assertEqual(response.status_code, 401)

        response = self.client.put(url, headers=headers, json=None)
        self.assertEqual(response.status_code, 400)

        response = self.client.put(url, headers=headers, json='qwerty')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(joke.as_dict, response.json)

        response = self.client.put(url, headers=headers, json='qwerty')
        self.assertEqual(response.status_code, 409)

    def test_view_delete_joke(self):
        joke = self.makeJoke()
        url = url_for('views.delete_joke', joke_id=joke.id)
        headers = dict(Authorization=joke.user.token)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

        response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, 204)
        self.assertNotIn(joke, Joke.query.all())
