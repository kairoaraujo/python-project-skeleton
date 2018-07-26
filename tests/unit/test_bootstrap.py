#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from unittest import TestCase
from unittest.mock import patch
from project_name.bootstrap import status
from project_name.bootstrap import execute
from sqlalchemy import exc
from project_name import app
import json


class TestBootstrap(TestCase):
    """Tests boootstrap.py"""

    @patch("project_name.bootstrap.APIKeys.query")
    def test_status_true(self, mock_apikeys_query):
        """Tests function status True return """

        mock_apikeys_query.all.return_value = []
        self.assertTrue(status())

    @patch("project_name.bootstrap.APIKeys.query")
    def test_status_false(self, mock_apikeys_query):
        """Tests function status False return """

        # if there is a user, status() should return False
        mock_apikeys_query.all.return_value = ["some_user"]
        self.assertFalse(status())

    @patch("project_name.bootstrap.APIKeys.query")
    def test_status_exceptions(self, mock_apikeys_query):
        """Tests function status exceptions """

        # if there is a user, status() should return False
        mock_apikeys_query.all.side_effect = [
            exc.OperationalError("statement", "params", "org")
        ]

        expected_output = {
            "message": "(builtins.str) org",
            "status": False
        }

        with app.app_context():
            response = status()

        self.assertEqual(json.loads(response.data), expected_output)

    @patch("project_name.bootstrap.add")
    @patch("project_name.bootstrap.status")
    def test_execute_payload_and_status_ok(self, mock_status, mock_add):
        """Tests function execute with payload and status ok"""

        mock_add.return_value = True
        mock_status.return_value = True
        payload_sample = {
            "username": "fakeusername",
            "methods": ["GET", "PUT", "POST", "DELETE", "ALL"]
        }

        self.assertTrue(execute(payload_sample))

    @patch("project_name.bootstrap.status")
    def test_execute_payload_not_ok(self, mock_status):
        """Tests function execute with payload and status ok"""

        mock_status.return_value = True

        # Payload missing key 'username'
        payload_sample = {
            "methods": ["GET", "PUT", "POST", "DELETE", "ALL"]
        }

        self.assertDictEqual(
            {"status": False, "message": "Invalid payload."},
            execute(payload_sample))

        # Payload missing key 'methods'
        payload_sample = {
            "username": "fakeusername"
        }

        self.assertDictEqual(
            {"status": False, "message": "Invalid payload."},
            execute(payload_sample))

    @patch("project_name.bootstrap.status")
    def test_execute_payload_ok_status_not_ok(self, mock_status):
        """Tests function execute with payload and status ok"""

        mock_status.return_value = False

        payload_sample = {
            "username": "fakeusername",
            "methods": ["GET", "PUT", "POST", "DELETE", "ALL"]
        }

        self.assertDictEqual(
            {
                "status": False,
                "message": "Bootstrap not allowed. Bootstrap already "
                           "implemented."
            },
            execute(payload_sample))
