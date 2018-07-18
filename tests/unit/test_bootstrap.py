#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from unittest import TestCase
from unittest.mock import patch
from project_name.bootstrap import status
from sqlalchemy import exc
from project_name import app
import json


class TestBootstrap(TestCase):
    """Tests boootstrap.py"""

    @patch('project_name.models.apikeys.APIKeys.query')
    def test_status_true(self, mock_apikeys_query):
        """Tests function status True return """

        mock_apikeys_query.all.return_value = []
        self.assertTrue(status())

    @patch('project_name.models.apikeys.APIKeys.query')
    def test_status_false(self, mock_apikeys_query):
        """Tests function status False return """

        # if there is a user, status() should return False
        mock_apikeys_query.all.return_value = ["some_user"]
        self.assertFalse(status())

    @patch('project_name.models.apikeys.APIKeys.query')
    def test_status_exceptions(self, mock_apikeys_query):
        """Tests function exceptions """

        # if there is a user, status() should return False
        mock_apikeys_query.all.side_effect = [
            exc.OperationalError("statement", "params", "org")
        ]

        expected_output = {
            "message": "(builtins.str) org [SQL: 'statement'] [parameters: "
                       "'params'] (Background on this error at: "
                       "http://sqlalche.me/e/e3q8)",
            "status": False
        }

        with app.app_context():
            response = status()

        self.assertEqual(json.loads(response.data), expected_output)


