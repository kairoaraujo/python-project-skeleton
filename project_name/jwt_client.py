#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
import jwt
import requests
from flask import jsonify
from project_name.utils import std_response
import json


def _private_key(private_cert_file=None):

    if private_cert_file is None:
        private_cert_file = "project_name/certs/id_rsa"

    try:
        with open(private_cert_file) as p_cf:
            return p_cf.read()

    except (FileNotFoundError, PermissionError, FileExistsError) as e:
        raise e


def _encode(payload, private_cert_file=None):
    """Encodes the payload using certs available in certs dir"""

    try:
        private_key = _private_key(private_cert_file)

    except(FileNotFoundError, PermissionError, FileExistsError) as e:
        raise e

    payload_encoded = jwt.encode(
        payload,
        private_key,
        algorithm="RS256")

    token = payload_encoded

    return token


def _run_request(method, url, json_token, verify):
    """Runs the requests module using JWT in different methods"""

    try:
        if method == "GET":
            result = requests.get(
                url,
                headers={"Content-Type": "application/json"},
                data=json_token,
                verify=verify
            )
            response = jsonify(result.json())
            response.status_code = result.status_code

        elif method == "POST":

            result = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json_token,
                verify=verify
            )
            response = jsonify(result.json())
            response.status_code = result.status_code

        elif method == "PUT":

            result = requests.put(
                url,
                headers={"Content-Type": "application/json"},
                data=json_token,
                verify=verify
            )
            response = jsonify(result.json())
            response.status_code = result.status_code

        elif method == "DELETE":

            result = requests.delete(
                url,
                headers={"Content-Type": "application/json"},
                data=json_token,
                verify=verify
            )

            response = jsonify(result.json())
            response.status_code = result.status_code

        else:
            response = jsonify(std_response(
                False,
                f"Invalid method: {method}."
            ))

            response.status_code = 400

    except (
            requests.exceptions.MissingSchema,
            requests.exceptions.ConnectionError) as e:

        response = jsonify(std_response(
            False,
            str(e)
        ))

        response.status_code = 500

    return response


def request(*args, **kargs):
    """Does external requests using JWT signature."""

    if (
            len(args) < 1 or
            not args[0] or
            not args[1]
    ):
        response = jsonify(std_response(
            False,
            "Method and URL are required."
        ))

        response.status_code = 400
        return response

    method = args[0]
    url = args[1]

    if "payload" not in kargs:
        response = jsonify(std_response(
            False,
            "Payload is required!"
        ))

        response.status_code = 400
        return response

    if "private_cert_file" not in kargs:
        private_cert_file = None

    else:
        private_cert_file = kargs["private_cert_file"]

    if "verify" not in kargs:
        verify = True

    else:
        verify = kargs["verify"]

    try:
        data = _encode(kargs["payload"], private_cert_file)

    except (FileNotFoundError, PermissionError, FileExistsError) as e:

        response = jsonify(std_response(
            False,
            str(e)
        ))

        response.status_code = 500

        return response

    else:
        json_token = json.dumps({"token": data.decode("utf-8")})
        response = _run_request(method, url, json_token, verify)

    return response
