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
