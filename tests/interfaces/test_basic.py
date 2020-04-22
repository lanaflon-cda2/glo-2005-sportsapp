import unittest

from flask_injector import FlaskInjector

from app import app
from tests.bindings import configure_test_database, configure_mock_modules


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        FlaskInjector(app=app, modules=[configure_test_database, configure_mock_modules])

        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()