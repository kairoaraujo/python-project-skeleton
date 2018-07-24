#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
from unittest import TestCase
import json
from project_name import version
from app import app


class TestMainNS(TestCase):
    """Test project_name API (main namespace)"""

    def setUp(self):
        """Setup tests"""
        app.config['TESTING'] = True
        self.test = app.test_client()

    def test_root_swagger(self):
        """Tests root endpoint (swagger)"""

        response = self.test.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>project_name API</title>", response.data)

    def test_version(self):
        """Tests /version endpoint"""

        expected_response = {
            "component-name": "project_name",
            "version": version
        }
        response = self.test.get("/api/v1/version")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_response, json.loads(response.data))
