#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
from unittest import TestCase
from project_name import db
from app import app
from project_name.constants.database import PROJECT_ROOT
import os
import json

TEST_DB = 'test.db'
DATABASE = os.path.join(
    PROJECT_ROOT, "project_name", "databases", TEST_DB)
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE


class TestAPIUsers(TestCase):
    """Test apiusers API"""

    def setUp(self):
        """Setup tests"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        db.create_all()
        self.test = app.test_client()

    def tearDown(self):
        """Tear down tests"""
        db.session.remove()
        db.drop_all()
        os.remove(SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "/"))

    def test_apiusers_get(self):
        """Tests /apiusers endpoint method GET"""

        # tests without bootstrap
        response = self.test.get("/api/v1/configuration/apiusers")
        self.assertEqual(response.status_code, 500)

        # perform boostrap with one user
        payload = {
            "username": "appadmin",
            "methods": ["ALL"]
        }

        # perform bootstrap
        response = self.test.post(
            "/api/v1/configuration/bootstrap",
            data=json.dumps(payload),
            content_type='application/json'
        )

        # tests if the user is authenticated
        headers = {
            "x-api-key": json.loads(response.data)["apikey"],
            "username": json.loads(response.data)["username"]
        }

        response = self.test.get(
            "/api/v1/configuration/apiusers",
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            b'{"appadmin": {"methods": ["GET", "POST", "PUT", "DELETE"]}}\n',
            response.data
        )

    def test_apiusers_invalid_username_headers(self):
        """Tests /apiusers endpoint method GET"""

        # tests without bootstrap
        response = self.test.get("/api/v1/configuration/apiusers")
        self.assertEqual(response.status_code, 500)

        # perform boostrap with one user
        payload = {
            "username": "appadmin",
            "methods": ["ALL"]
        }

        # perform bootstrap
        response = self.test.post(
            "/api/v1/configuration/bootstrap",
            data=json.dumps(payload),
            content_type='application/json'
        )

        # tests if the user is authenticated
        headers = {
            "x-api-key": json.loads(response.data)["apikey"],
            "username": "idontexist"
        }

        response = self.test.get(
            "/api/v1/configuration/apiusers",
            headers=headers
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            b'{"message":"Username not found","status":false}\n',
            response.data
        )

    def test_apiusers_post(self):
        """Tests /apiusers endpoint method POST"""
        payload = {
            "username": "appadmin",
            "method": ["ALL"]
        }
        response = self.test.post(
            "/api/v1/configuration/apiusers",
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 500)

        # perform boostrap with one user
        payload = {
            "username": "appadmin",
            "methods": ["ALL"]
        }

        # perform bootstrap
        response = self.test.post(
            "/api/v1/configuration/bootstrap",
            data=json.dumps(payload),
            content_type='application/json'
        )

        # tests if the user is authenticated
        headers = {
            "x-api-key": json.loads(response.data)["apikey"],
            "username": json.loads(response.data)["username"]
        }

        payload = {
            "username": "kairo",
            "methods": ["GET", "POST"]
        }

        response = self.test.post(
            "/api/v1/configuration/apiusers",
            headers=headers,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'{"apikey":', response.data)
        self.assertIn(b'"methods":["GET","POST"]',
                      response.data)
        self.assertIn(b'"username":"kairo"}\n', response.data)
        self.assertEqual(response.status_code, 201)

    def test_apiusers_username_get(self):
        """Tests /apiusers/<username> endpoint method GET"""

        # perform boostrap with one user
        payload = {
            "username": "appadmin",
            "methods": ["ALL"]
        }

        # perform bootstrap
        response = self.test.post(
            "/api/v1/configuration/bootstrap",
            data=json.dumps(payload),
            content_type='application/json'
        )

        # tests if the user is authenticated
        headers = {
            "x-api-key": json.loads(response.data)["apikey"],
            "username": json.loads(response.data)["username"]
        }

        payload = {
            "username": "kairo",
            "methods": ["GET", "POST"]
        }

        response = self.test.post(
            "/api/v1/configuration/apiusers",
            headers=headers,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'{"apikey":', response.data)
        self.assertIn(b'"methods":["GET","POST"]',
                      response.data)
        self.assertIn(b'"username":"kairo"}\n', response.data)
        self.assertEqual(response.status_code, 201)

        response = self.test.get(
            "/api/v1/configuration/apiusers/kairo",
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            b'{"kairo": {"methods": ["GET", "POST"]}}\n',
            response.data
        )

    def test_apiusers_username_get_not_ok(self):
        """Tests /apiusers/<username> endpoint method GET HTTP_CODE 500"""

        response = self.test.get("/api/v1/configuration/apiusers/username")
        self.assertEqual(response.status_code, 500)

    def test_apiusers_username_put(self):
        """Tests /apiusers endpoint method POST"""

        # perform boostrap
        payload = {
            "username": "appadmin",
            "methods": ["ALL"]
        }

        response = self.test.post(
            "/api/v1/configuration/bootstrap",
            data=json.dumps(payload),
            content_type='application/json'
        )

        # tests if the user is authenticated and adds user kairo
        headers = {
            "x-api-key": json.loads(response.data)["apikey"],
            "username": json.loads(response.data)["username"]
        }

        payload = {
            "username": "kairo",
            "methods": ["GET", "POST"]
        }

        response = self.test.post(
            "/api/v1/configuration/apiusers",
            headers=headers,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'{"apikey":', response.data)
        self.assertIn(b'"methods":["GET","POST"]',
                      response.data)
        self.assertIn(b'"username":"kairo"}\n', response.data)
        self.assertEqual(response.status_code, 201)

        payload = {
            "methods": ["GET", "POST", "PUT"],
            "apikey": True
        }

        response = self.test.put(
            "/api/v1/configuration/apiusers/kairo",
            data=json.dumps(payload),
            headers=headers,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'{"apikey":', response.data)
        self.assertIn(b'"methods":["GET","POST","PUT"]',
                      response.data)

    def test_apiusers_username_put_nok(self):
        """Tests /apiusers endpoint method POST HTTP_CODE 500"""
        payload = {
            "methods": ["GET", "POST"],
            "apikey": True
        }
        response = self.test.put(
            "/api/v1/configuration/apiusers/username",
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 500)
