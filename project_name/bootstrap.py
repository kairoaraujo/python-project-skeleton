#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
from project_name.models.apikeys import APIKeys
from project_name.utils import std_response
from constants.methods import ALLOWED_METHODS
from project_name.apiusers import add_apiuser


def _validate_methods(methods):
    """Validates methods allowed"""

    for method in methods:
        if method not in ALLOWED_METHODS:
            return False

    return True


def status():
    """Gets bootstrap status """
    users = APIKeys.query.all()

    if len(users) == 0:
        return True

    else:
        return False


def execute(payload):
    """Executes bootstrap"""

    if (
        "username" and "methods" in payload and
        type(payload["methods"]) is list
    ):

        if status():
            response = add_apiuser(payload)
            return response

        else:

            return std_response(
                False,
                "Bootstrap not allowed. Bootstrap already implemented."
                )

    else:

        return std_response(False, "Invalid payload.")
