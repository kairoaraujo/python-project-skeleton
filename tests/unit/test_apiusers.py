#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from unittest import TestCase
from unittest.mock import patch
from project_name import app
from project_name.apiusers import _validate_methods
from project_name.apiusers import get
from project_name.apiusers import get_methods
from project_name.apiusers import get_methods_keys
from project_name.apiusers import add
from project_name.apiusers import update
from sqlalchemy import exc
import json


class FakeAttributes(dict):
    pass


class TestAPIUsers(TestCase):
    """Tests apiusers module"""

    def setUp(self):
        """Sets up for tests"""

        self.appadmin = FakeAttributes()
        self.appadmin.username = "appadmin"
        self.appadmin.methods = "['GET', 'PUT', 'POST', 'DELETE']"
        self.appadmin.apikey = 'appadminapikey'

        self.kairo = FakeAttributes()
        self.kairo.username = "kairo"
        self.kairo.methods = '["GET"]'
        self.kairo.apikey = 'kairoapikey'

    def test__validate_methods(self):
        """Tests internal validate_methods"""

        self.assertTrue(_validate_methods(["GET", "PUT", "POST", "DELETE"]))
        self.assertTrue(_validate_methods(["ALL"]))
        self.assertFalse(_validate_methods(["INVALID_METHOD"]))
        self.assertFalse(_validate_methods("STRING"))

    @patch("project_name.apiusers.APIKeys.query")
    def test_get(self, mock_apikeys_query):
        """Tests function get that returns users from SQLite"""

        expected_response = ["appadmin", "kairo"]
        mock_apikeys_query.all.return_value = expected_response
        self.assertEqual(get(), expected_response)

        # TODO test when username is specified

    @patch("project_name.apiusers.get")
    def test_get_methods(self, mock_get):
        """Tests function get_methods"""

        # TODO should have the username, it is not working fully but tests
        mock_get.return_value = self.appadmin
        self.assertDictEqual(
            {'{}': {'methods': ['GET', 'PUT', 'POST', 'DELETE']}},
            get_methods("appadmin")
        )

        mock_get.return_value = [self.kairo, self.appadmin]
        self.assertDictEqual(
            {'{}': {'methods': ['GET', 'PUT', 'POST', 'DELETE']}},
            get_methods()
        )

        with app.app_context():
            mock_get.return_value = None
            response = get_methods()
            self.assertDictEqual(
                json.loads(response.data),
                {'message': 'Username not found', 'status': False}
            )

    @patch("project_name.apiusers.get")
    def test_get_method_keys(self, mock_get):
        """Tests function get_method_key"""

        # TODO should have the username, it is not working fully but tests
        mock_get.return_value = self.appadmin
        self.assertDictEqual(
            {
                '{}': {
                    'apikey': 'appadminapikey',
                    'methods': ['GET', 'PUT', 'POST', 'DELETE']
                }
            },
            get_methods_keys("appadmin")
        )

        with app.app_context():
            mock_get.return_value = None
            response = get_methods_keys('xxxxx')
            self.assertDictEqual(
                json.loads(response.data),
                {'message': 'Username not found', 'status': False}
            )

    @patch("project_name.apiusers.db")
    def test_add_ok(self, mock_db):
        """Tests function add"""

        test_payload = {
            "username": "testuser",
            "methods": ["GET", "PUT", "POST"]
        }

        mock_db.session.add.return_value = True
        mock_db.session.commit.return_value = True

        with app.app_context():
            self.assertEqual(add(test_payload).status_code, 201)

        test_payload = {
            "username": "testuser",
            "methods": ["ALL"]
        }

        with app.app_context():
            self.assertEqual(add(test_payload).status_code, 201)

    def test_add_invalid_payload(self):
        """Tests function add with a wrong payload"""

        # missing 'username'
        test_payload = {
            "methods": ["GET", "PUT", "POST"]
        }

        with app.app_context():
            response = add(test_payload)
            self.assertEqual(response.status_code, 400)
            self.assertDictEqual(
                json.loads(response.data),
                {
                    "status": False,
                    "message": "'username' and 'methods' are required."
                }
            )

        # missing 'methods'
        test_payload = {
            "username": "testuser"
        }

        with app.app_context():
            response = add(test_payload)
            self.assertEqual(response.status_code, 400)
            self.assertDictEqual(
                json.loads(response.data),
                {
                    "status": False,
                    "message": "'username' and 'methods' are required."
                }
            )

    def test_add_invalid_method(self):
        """Tests function add with an invalid method"""

        test_payload = {
            "username": "testuser",
            "methods": ["GET", "XXX", "POST"]
        }

        with app.app_context():
            response = add(test_payload)
            self.assertEqual(response.status_code, 400)
            self.assertDictEqual(
                json.loads(response.data),
                {
                    "status": False,
                    "message": "Invalid method(s)."
                }
            )

    @patch("project_name.apiusers.db")
    def test_add_exceptions(self, mock_db):
        """Tests function add exceptions"""

        test_payload = {
            "username": "testuser",
            "methods": ["GET", "PUT", "POST"]
        }

        mock_db.session.add.return_value = True
        mock_db.session.commit.side_effect = exc.IntegrityError(
            "statement", "params", "orig"
        )

        with app.app_context():
            response = add(test_payload)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                json.loads(response.data),
                {
                    "status": False,
                    "message": "username already exists. ERROR:(builtins.str) "
                               "orig [SQL: 'statement'] [parameters: 'params']"
                               " (Background on this error at: "
                               "http://sqlalche.me/e/gkpj)"
                }
            )

    @patch("project_name.apiusers.secrets.token_hex")
    @patch("project_name.apiusers.db")
    @patch("project_name.apiusers.get")
    def test_update_ok(self, mock_get, mock_db, mock_token):
        """Tests function update"""

        # new methods
        test_payload = {
            "methods": ["GET", "PUT", "POST", "DELETE"],
            "apikey": True
        }
        username = "kairo"
        mock_get.return_value = self.kairo
        mock_db.session.return_value = True
        mock_token.return_value = "new_api_key"

        with app.app_context():
            response = update(test_payload, username)
            self.assertEqual(response.status_code, 201)
            self.assertDictEqual(
                json.loads(response.data),
                {
                    username: {
                        "methods": ["GET", "PUT", "POST", "DELETE"],
                        "apikey": "new_api_key"
                    }
                }
            )

        # tests method "ALL"
        test_payload = {
            "methods": ["ALL"]
        }
        username = "kairo"
        mock_get.return_value = self.kairo
        mock_db.session.return_value = True

        with app.app_context():
            response = update(test_payload, username)
            self.assertEqual(response.status_code, 201)
            self.assertDictEqual(
                json.loads(response.data),
                {
                    username: {
                        "methods": ["GET", "POST", "PUT", "DELETE"]
                    }
                }
            )

        # tests same methods
        test_payload = {
            "methods": ["GET", "PUT", "POST", "DELETE"]
        }

        username = "appadmin"
        mock_get.return_value = self.appadmin
        mock_db.session.return_value = True

        with app.app_context():
            response = update(test_payload, username)
            self.assertEqual(response.status_code, 201)
            self.assertDictEqual(
                json.loads(response.data),
                {
                    username: {
                        "methods": "No changes. Same methods."
                    }
                }
            )

    @patch("project_name.apiusers.get")
    def test_update_invalid_method(self, mock_get):
        """Tests function update with an invalid method"""

        test_payload = {
            "methods": ["GET", "PUT", "POST", "INVALID"]
        }
        username = "appadmin"
        mock_get.return_value = ['appadmin']
        with app.app_context():
            response = update(test_payload, username)
            self.assertEqual(response.status_code, 400)
            self.assertDictEqual(
                json.loads(response.data),
                {
                    "status": False,
                    "message": "Invalid method(s)."
                }
            )

    @patch("project_name.apiusers.get")
    def test_update_invalid_payload(self, mock_get):
        """Tests function update with an invalid payload"""

        test_payload = {}
        username = "appadmin"
        mock_get.return_value = ['appadmin']
        with app.app_context():
            response = update(test_payload, username)
            self.assertEqual(response.status_code, 400)
            self.assertDictEqual(
                json.loads(response.data),
                {
                    "status": False,
                    "message": "'methods' or 'apikey' is required in payload."
                }
            )

    @patch("project_name.apiusers.get")
    def test_update_invalid_user(self, mock_get):
        """Tests function update with an invalid user"""

        test_payload = {}
        username = 'appadmin'
        mock_get.return_value = None
        with app.app_context():
            response = update(test_payload, username)
            self.assertEqual(response.status_code, 400)
            self.assertDictEqual(
                json.loads(response.data),
                {
                    "status": False,
                    "message": "Username not found."
                }
            )

    @patch("project_name.apiusers.db")
    def test_update_exceptions(self, mock_db):
        """Tests function update exceptions"""

        username = 'appadmin'
        test_payload = {
            "methods": ["GET", "PUT", "POST", "DELETE"],
            "apikey": True
        }
        mock_db.session.commit.side_effect = exc.OperationalError(
            "statement", "params", "orig"
        )

        with app.app_context():
            response = update(test_payload, username)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(
                json.loads(response.data),
                {
                    "status": False,
                    "message": "(builtins.str) "
                               "orig [SQL: 'statement'] [parameters: 'params']"
                               " (Background on this error at: "
                               "http://sqlalche.me/e/e3q8)"
                }
            )
