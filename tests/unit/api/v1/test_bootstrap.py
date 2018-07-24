#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
from unittest import TestCase
from project_name import db
from app import app
from constants.database import PROJECT_ROOT
import json
import os

TEST_DB = 'test.db'
DATABASE = os.path.join(
    PROJECT_ROOT, "project_name", "databases", TEST_DB)
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE


class TestBootstrap(TestCase):
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

    def test_boostrap_get(self):
        """Tests endpoint boostrap method GET"""

        response = self.test.get("/api/v1/configuration/bootstrap")
        expected_response = {
            "status": True,
            "message": "Bootstrap is available to be configured."
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response, json.loads(response.data))

    def test_bootstrap_post(self):
        """Tests /apiusers endpoint method POST"""
        payload = {
            "username": "appadmin",
            "methods": ["ALL"]
        }

        # Tests bootstrap
        response = self.test.post(
            "/api/v1/configuration/bootstrap",
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertIn(b'{"apikey":', response.data)
        self.assertIn(b'"methods":["GET","POST","PUT","DELETE"]',
                      response.data)
        self.assertIn(b'"username":"appadmin"}\n', response.data)
        self.assertEqual(response.status_code, 201)

        # Tests GET boostrap after configuration
        response = self.test.get("/api/v1/configuration/bootstrap")
        expected_response = {
            "status": False,
            "message": "Bootstrap not available. Bootstrap already done."
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response, json.loads(response.data))
