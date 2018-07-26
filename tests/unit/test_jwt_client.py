#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from unittest import TestCase
from unittest.mock import patch, mock_open
from project_name.constants.methods import ALLOWED_METHODS
from project_name.jwt_client import (
    _private_key,
    _encode,
    _run_request,
    request
)
import jwt
import json
from app import app
from requests.exceptions import MissingSchema, ConnectionError


class TestJWTClient(TestCase):
    """Tests JWT Client"""

    def setUp(self):
        """Setup tests"""

        self.private_key_file = "tests/unit/constants/fake_id_rsa"
        self.public_key_file = "tests/unit/constants/fake_id_rsa.pub"

        with open(self.private_key_file) as fake_priv_cf:
            self.private_key = fake_priv_cf.read()

        with open(self.public_key_file) as fake_pub_cf:
            self.fake_public_key = fake_pub_cf.read()

        self.payload = {"key": "value"}

        class FakeObj:
            pass

            def json(self):
                return {"hello}": "world"}

        self.fake_requests_resp = FakeObj()

    def _decode_test(self, payload):
        """Decodes the JWT toke for test proposes"""

        return jwt.decode(
            payload,
            self.fake_public_key,
            algorithms='RS256'
        )

    @patch("builtins.open")
    def test__private_key(self, mock_file):
        """Tests internal function _private_key"""
        mock_open(mock_file, self.private_key)

        response = _private_key()
        self.assertEqual(response, self.private_key)

        response = _private_key("my_special_file")
        self.assertEqual(response, self.private_key)

    @patch("builtins.open")
    def test__private_key_exceptions(self, mock_file):
        """Tests internal function _private_key exceptions"""

        mock_file.side_effect = [
            FileNotFoundError, PermissionError, FileExistsError
        ]

        with self.assertRaises(FileNotFoundError) as e:
            self.assertEqual(_private_key(), e)

        with self.assertRaises(PermissionError) as e:
            self.assertEqual(_private_key(), e)

        with self.assertRaises(FileExistsError) as e:
            self.assertEqual(_private_key(), e)

    @patch("project_name.jwt_client._private_key")
    def tests__encode(self, mock_private_key):
        """Tests internal function _encode"""

        mock_private_key.return_value = self.private_key
        payload = _encode(self.payload)
        self.assertEqual(self._decode_test(payload), self.payload)

    @patch("project_name.jwt_client._private_key")
    def tests__encode_exceptions(self, mock_private_key):
        """Tests internal function _encode"""

        mock_private_key.side_effect = [
            FileNotFoundError, PermissionError, FileExistsError
        ]

        with self.assertRaises(FileNotFoundError) as e:
            self.assertEqual(_encode(self.payload), e)

        with self.assertRaises(PermissionError) as e:
            self.assertEqual(_encode(self.payload), e)

        with self.assertRaises(FileExistsError) as e:
            self.assertEqual(_encode(self.payload), e)

    @patch("project_name.jwt_client.requests")
    def test__run_request(self, mock_requests):
        """Tests function _run_request"""

        self.fake_requests_resp.status_code = 200
        mock_requests.get.return_value = self.fake_requests_resp
        mock_requests.post.return_value = self.fake_requests_resp
        mock_requests.put.return_value = self.fake_requests_resp
        mock_requests.delete.return_value = self.fake_requests_resp

        for method in ALLOWED_METHODS:
            print(f"Testing {method}")
            if method == "ALL":
                self.fake_requests_resp.status_code = 400
            with app.app_context():
                response = _run_request(
                    method,
                    "http://fake.url",
                    json.dumps(self.payload),
                    verify=True
                )

            if method == "ALL":
                self.assertEqual(
                    b'{"message":"Invalid method: ALL.","status":false}\n',
                    response.data
                )
                self.assertEqual(response.status_code, 400)

            else:
                self.assertEqual(b'{"hello}":"world"}\n', response.data)
                self.assertEqual(response.status_code, 200)

    @patch("project_name.jwt_client.requests.get")
    def test__run_request_exceptions(self, mock_requests):
        """Tests function requests exceptions"""

        exceptions = [MissingSchema, ConnectionError]
        mock_requests.side_effect = exceptions

        for exception in exceptions:
            print(f"Testing {str(exception)}")
            with app.app_context():
                response = _run_request(
                    "GET",
                    "http://fake.url",
                    json.dumps(self.payload),
                    verify=True
                )
            self.assertEqual(response.status_code, 500)

    def test_request_no_url_method(self):
        """Tests function request without url"""

        payload = {"key": "value"}

        with app.app_context():
            response = request(payload=payload, verify=False)

        self.assertEqual(response.status_code, 400)

    @patch("project_name.jwt_client._run_request")
    @patch("project_name.jwt_client._encode")
    def test_request(self, mock_encode, mock_run_request):
        """Tests function request"""

        method = "GET"
        url = "http://fake.url"
        payload = {"key": "value"}

        _encode_return = _encode(self.payload, self.private_key_file)
        mock_encode.return_value = _encode_return

        self.fake_requests_resp.status_code = 200
        mock_run_request.return_value = self.fake_requests_resp

        response = request(method, url, payload=payload, verify=False)
        self.assertEqual(response.status_code, 200)

    def test_request_no_payload(self):
        """Tests function request without payload"""

        method = "GET"
        url = "http://fake.url"

        with app.app_context():
            response = request(method, url, verify=False)

        self.assertEqual(response.status_code, 400)

    @patch("project_name.jwt_client._run_request")
    @patch("project_name.jwt_client._encode")
    def test_request_spec_cert_file_no_verify(self, mock_encode,
                                              mock_run_request):
        """Tests function request specifying cert file and without verify"""

        method = "GET"
        url = "http://fake.url"
        payload = {"key": "value"}

        _encode_return = _encode(self.payload, self.private_key_file)
        mock_encode.return_value = _encode_return

        self.fake_requests_resp.status_code = 200
        mock_run_request.return_value = self.fake_requests_resp

        response = request(
            method, url, payload=payload,
            private_cert_file=self.private_key_file)
        self.assertEqual(response.status_code, 200)

    @patch("project_name.jwt_client._encode")
    def test_request_exceptions(self, mock_encode):
        """Tests function request exceptions"""

        method = "GET"
        url = "http://fake.url"
        payload = {"key": "value"}

        exceptions = [FileNotFoundError, PermissionError, FileExistsError]
        mock_encode.side_effect = exceptions

        for exception in exceptions:
            print(f"Testing {exception}")
            with app.app_context():
                response = request(
                    method, url, payload=payload,
                    private_cert_file=self.private_key_file)

            self.assertEqual(response.status_code, 500)
