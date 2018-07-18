#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
import ast
import secrets
from flask import jsonify
from project_name import db
from project_name.models.apikeys import APIKeys
from constants.methods import ALLOWED_METHODS
from sqlalchemy import exc
from project_name import utils


def _validate_methods(methods):
    """Validates methods allowed"""

    for method in methods:
        if method not in ALLOWED_METHODS:
            return False

    return True


def get(username=None):
    """Return users from SQLite databse"""

    if username is None:
        apiusers = APIKeys.query.all()

    else:
        apiusers = APIKeys.query.filter_by(username=username).first()

    return apiusers


def get_methods(username=None):

    apiusers = get(username)
    response = {}

    if username is None:
        for apiuser in apiusers:
            response[str(apiuser)] = {"methods": ast.literal_eval(
                apiuser.methods)}
    else:
        if apiusers is None:
            response = jsonify(utils.std_response(False, "Username not found"))
            response.status_code = 404
        else:
            response[str(apiusers)] = {"methods": ast.literal_eval(
                apiusers.methods)}

    return response


def get_method_keys(username):
    apiusers = get(username)
    response = {}

    if username is None:
        for apiuser in apiusers:
            response[str(apiuser)] = {
                "apikey": apiuser.apikey,
                "methods": ast.literal_eval(apiuser.methods)
            }

    else:
        response[str(apiusers)] = {
            "apikey": apiusers.apikey,
            "methods": ast.literal_eval(apiusers.methods)
        }

    return response


def add(payload):
    """Adds API user"""

    if "username" and "methods" not in payload:
        response = jsonify(
            utils.std_response(
                False, "'username' and 'methods' are required."
            )
        )
        response.status_code = 501

        return response

    username = payload["username"]
    methods = payload["methods"]

    if not _validate_methods(methods):
        return utils.std_response(False, "Invalid methods")

    if "ALL" in methods:
        methods = ALLOWED_METHODS
        methods.remove("ALL")

    try:
        api_key = secrets.token_hex(32)
        api_user = APIKeys(username, api_key, True, f"{methods}")
        db.session.add(api_user)
        db.session.commit()

    except exc.OperationalError as e:
        return utils.std_response(False, str(e))

    except exc.IntegrityError as e:
        return utils.std_response(
            False,
            {
                "message": "username already exists.",
                "error": str(e)
            }
        )

    response = jsonify({
        "username": str(api_user),
        "apikey": api_key,
        "methods": methods
    })

    response.status_code = 201

    return response


def update(payload, username):
    """Updates API user data"""

    response = {}
    api_user = get(username)

    if api_user is None:
        response = jsonify(utils.std_response(False, "Username not found."))
        response.status_code = 404

        return response

    response[username] = {}

    if "methods" not in payload and "apikey" not in payload:
        response = jsonify(
            utils.std_response(
                False, "'methods' or 'apikey' is required in payload."
            )
        )
        response.status_code = 501

        return response

    if "methods" in payload:
        methods = payload["methods"]

        if not _validate_methods(methods):
            response = jsonify(utils.std_response(False, "Invalid method."))
            response.status_code = 501

            return response

        if "ALL" in methods:
            methods = ALLOWED_METHODS
            methods.remove("ALL")

        if api_user.methods == f"{methods}":
            response[username]["methods"] = "No changes. Same methods."

        else:
            # update the methods
            api_user.methods = f"{methods}"

            response[username]["methods"] = methods

    if "apikey" in payload and payload["apikey"]:
        api_key = secrets.token_hex(32)

        # update the api key
        api_user.apikey = api_key
        response[username]["apikey"] = api_key

    try:
        # commit
        db.session.commit()
        response = jsonify(response)
        response.status_code = 201

    except exc.OperationalError as e:

        response = jsonify(utils.std_response(False, str(e)))
        response.status_code = 500

    return response
