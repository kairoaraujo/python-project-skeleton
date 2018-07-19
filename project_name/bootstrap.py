#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from flask import jsonify
from project_name.models.apikeys import APIKeys
from project_name import utils
from project_name.apiusers import add
from sqlalchemy import exc


def status():
    """Gets bootstrap status """
    try:
        users = APIKeys.query.all()

    except exc.OperationalError as e:
        response = jsonify(utils.std_response(False, str(e)))
        response.status_code = 500

        return response

    if len(users) == 0:
        return True

    else:
        return False


def execute(payload):
    """Executes bootstrap"""

    if (
        "username" in payload and
        "methods" in payload and
        type(payload["methods"]) is list
    ):

        if status():
            response = add(payload)
            return response

        else:

            return utils.std_response(
                False,
                "Bootstrap not allowed. Bootstrap already implemented."
                )

    else:

        return utils.std_response(False, "Invalid payload.")
