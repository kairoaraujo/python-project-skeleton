#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
import ast
import secrets
from project_name import db
from project_name.models.apikeys import APIKeys
from constants.methods import ALLOWED_METHODS
from sqlalchemy import exc
from project_name import utils


def get_apiusers(username=None):
    """Return users from SQLite databse"""

    if username is None:
        apiusers = APIKeys.query.all()

    else:
        apiusers = APIKeys.query.filter_by(username=username).first()

    return apiusers


def get_apiusers_methods(username=None):

    apiusers = get_apiusers(username)
    response = {}

    if username is None:
        for apiuser in apiusers:
            response[str(apiuser)] = {"methods": ast.literal_eval(
                apiuser.methods)}
    else:
        response[str(apiusers)] = {"methods": ast.literal_eval(
            apiusers.methods)}

    return response


def get_apiusers_method_keys(username):
    apiusers = get_apiusers(username)
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


def add_apiuser(payload):
    """Executes bootstrap"""

    username = payload["username"]
    methods = payload["methods"]

    if not utils._validate_methods(methods):
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

    response = {
        "username": str(api_user),
        "apikey": api_key,
        "methods": methods
    }

    return response
