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

import json


class FakeAttributes(dict):
    pass


class TestAPIUsers(TestCase):
    """Tests apiusers module"""

    def setUp(self):
        """Sets up for tests"""

        self.appadmin = FakeAttributes()
        self.appadmin.username = "appadmin"
        self.appadmin.methods = '["GET", "PUT", "POST", "DELETE"]'
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
        """Tests the function add"""

        test_payload = {
            "username": "testuser",
            "methods": ["GET", "PUT", "POST"]
        }

        mock_db.session.add.return_value = True
        mock_db.session.commit.return_value = True

        with app.app_context():
            self.assertEqual(add(test_payload).status_code, 201)
