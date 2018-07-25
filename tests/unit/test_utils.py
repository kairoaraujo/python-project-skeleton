#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from unittest import TestCase
from project_name import utils


class TestUtils(TestCase):
    """Tests the utils."""

    def test_std_response_ok(self):
        """Tests std_response function."""

        expected_response = {"status": True, "message": "OK"}
        response = utils.std_response(True, "OK")

        self.assertEqual(response, expected_response)

    def test_validate_methods(self):
        """Tests internal validate_methods"""

        self.assertTrue(
            utils.validate_methods(["GET", "PUT", "POST", "DELETE"]))
        self.assertTrue(utils.validate_methods(["ALL"]))
        self.assertFalse(utils.validate_methods(["INVALID_METHOD"]))
        self.assertFalse(utils.validate_methods("STRING"))
