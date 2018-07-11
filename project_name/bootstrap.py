#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
from project_name.models.apikeys import APIKeys
from project_name.utils import std_response
from project_name import db
from constants.bootstrap import ALLOWED_METHODS
from sqlalchemy import exc
import secrets


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

        username = payload["username"]
        methods = payload["methods"]
        if not _validate_methods(methods):
            return std_response(False, "Invalid methods")

        if "ALL" in methods:
            methods = ALLOWED_METHODS
            methods.remove("ALL")

        if status():
            try:
                api_key = secrets.token_hex(32)
                api_user = APIKeys(username, api_key, True, f"{methods}")
                db.session.add(api_user)
                db.session.commit()

            except exc.OperationalError as e:

                return std_response(False, e)

            response = {
                "username": str(api_user),
                "apikey": api_key,
                "methods": methods
            }

            return response

        else:

            return std_response(
                False,
                "Bootstrap not allowed. Bootstrap already implemented."
                )

    else:

        return std_response(False, "Invalid payload.")


