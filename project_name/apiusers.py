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
from sqlalchemy import exc
from project_name import utils
from project_name.constants.methods import ALLOWED_METHODS


def get(username=None):
    """Return users from SQLite database"""

    if username is None:
        apiusers = APIKeys.query.all()

    else:
        apiusers = APIKeys.query.filter_by(username=username).first()

    return apiusers


def get_methods(username=None):
    """Gets the user's methods"""

    apiusers = get(username)
    response = {}

    if apiusers is None:
        response = jsonify(utils.std_response(False, "Username not found"))
        response.status_code = 404

    elif type(apiusers) is list:
        for apiuser in apiusers:
            response[str(apiuser)] = {"methods": ast.literal_eval(
                apiuser.methods)}
    else:
        response[str(apiusers)] = {"methods": ast.literal_eval(
            apiusers.methods)}

    return response


def get_methods_keys(username):
    apiusers = get(username)
    response = {}

    if apiusers is None:
        response = jsonify(utils.std_response(False, "Username not found"))
        response.status_code = 404

    elif type(apiusers) is list:
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

    if "username" not in payload or "methods" not in payload:
        response = jsonify(
            utils.std_response(
                False, "'username' and 'methods' are required."
            )
        )
        response.status_code = 400

        return response

    username = payload["username"]
    methods = payload["methods"]

    if "ALL" in methods:
        methods = ALLOWED_METHODS.copy()
        methods.remove("ALL")

    if not utils.validate_methods(methods):
        response = jsonify(utils.std_response(False, "Invalid method(s)."))
        response.status_code = 400

        return response

    try:
        if "apikey" in payload and payload["apikey"]:
            api_key = payload["apikey"]
        else:
            api_key = secrets.token_hex(32)
        api_user = APIKeys(username, api_key, True, f"{methods}")
        db.session.add(api_user)
        db.session.commit()

    except exc.IntegrityError as e:
        response = jsonify(
            utils.std_response(
                False,
                "username already exists. ERROR:" +
                str(e).split("[")[0].strip()
            )
        )
        response.status_code = 400

        return response

    except exc.OperationalError as e:
            response = jsonify(
                utils.std_response(False, str(e).split("[")[0].strip())
            )
            response.status_code = 500

            return response

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
        response.status_code = 400

        return response

    response[username] = {}

    if "methods" not in payload and "apikey" not in payload:
        response = jsonify(
            utils.std_response(
                False, "'methods' or 'apikey' is required in payload."
            )
        )
        response.status_code = 400

        return response

    if "methods" in payload:
        methods = payload["methods"]

        if "ALL" in methods:
            methods = ALLOWED_METHODS.copy()
            methods.remove("ALL")

        if not utils.validate_methods(methods):
            response = jsonify(utils.std_response(False, "Invalid method(s)."))
            response.status_code = 400

            return response

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
        response = jsonify(utils.std_response(
            False, str(e).split("[")[0].strip()))
        response.status_code = 500

        return response

    return response
