from jokes_api import cli
from jokes_api.models import User

from tests import TestApp


class CliTest(TestApp):

    def setUp(self):
        super().setUp()
        self.click = self.app.test_cli_runner()

    def test_cli_user_show(self):
        user = self.makeUser(username='test')
        result = self.click.invoke(cli.user_show)

        self.assertIsNone(result.exception)
        self.assertEqual(result.exit_code, 0)
        self.assertIn(user.username, result.output)
        self.assertIn(user.token, result.output)

    def test_cli_user_create(self):
        result = self.click.invoke(cli.user_create, ['test'])
        self.assertIsNone(result.exception)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(User.query.get('test'))

        result = self.click.invoke(cli.user_create, ['test'])
        self.assertIsNotNone(result.exception)
        self.assertEqual(result.exit_code, 1)  # already exist

    def test_cli_user_delete(self):
        result = self.click.invoke(cli.user_delete, ['test'])
        self.assertIsNotNone(result.exception)
        self.assertEqual(result.exit_code, 1)  # not found

        self.makeUser(username='test')
        result = self.click.invoke(cli.user_delete, ['test'])
        self.assertIsNone(result.exception)
        self.assertEqual(result.exit_code, 0)
        self.assertFalse(User.query.get('test'))

    def test_cli_user_reset(self):
        result = self.click.invoke(cli.user_reset, ['test'])
        self.assertIsNotNone(result.exception)
        self.assertEqual(result.exit_code, 1)  # not found

        before_refresh = self.makeUser(username='test').token
        result = self.click.invoke(cli.user_reset, ['test'])
        after_refresh = User.query.get('test').token
        self.assertIsNone(result.exception)
        self.assertEqual(result.exit_code, 0)
        self.assertNotEqual(before_refresh, after_refresh)
