#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
from unittest import TestCase
from unittest.mock import patch
from app import app
import json
from project_name import db
from project_name.constants.database import PROJECT_ROOT
import os

TEST_DB = 'test.db'
DATABASE = os.path.join(
    PROJECT_ROOT, "project_name", "databases", TEST_DB)
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE


class TestJWTCalls(TestCase):
    """Test JWT Calls API"""

    def setUp(self):
        """Setup tests"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.test = app.test_client()

        class FakeObj:
            pass

            def data(self):
                json.dumps({"hello": "world"})

        self.fake_response = FakeObj

    def tearDown(self):
        """Tear down tests"""
        db.session.remove()
        db.drop_all()
        os.remove(SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "/"))

    @patch("project_name.jwt_client.request")
    def test_wwwmockio_post(self, mock_jwt_request):
        """Tests endpoint wwwmockio"""

        mock_jwt_request.return_value = {"hello": "world"}

        data = json.dumps({"key": "value"})
        response = self.test.post(
            "/api/v1/calls/www_mocky_io",
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.data,
            b'{"message":"System without bootstrap.","status":false}\n'
        )

        # bootstrap
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        payload = {
            "username": "appadmin",
            "methods": ["ALL"]
        }
        db.create_all()
        bootstrap = self.test.post(
            "/api/v1/configuration/bootstrap",
            data=json.dumps(payload),
            content_type='application/json'
        )

        headers = {
            "x-api-key": json.loads(bootstrap.data)["apikey"],
            "username": "appadmin"
        }

        response = self.test.post(
            "/api/v1/calls/www_mocky_io",
            headers=headers,
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.data, b'{"hello": "world"}\n')
        self.assertEqual(response.status_code, 200)
