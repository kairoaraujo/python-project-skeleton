#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
import ast
from functools import wraps
from flask import request, abort
from project_name import db
from project_name.models.apikeys import APIKeys


def std_response(state, message):
    """Returns a standard dict response """

    response = {
        "status": state,
        "message": message
    }

    return response


def get_users(username=None)
    """Return users from SQLite databse"""

    if username is None:
        users = APIKeys.query.all()

    else:
        users = APIKeys.query.filter_by(username=username)

    return users


def get_users_methods(username=None):
    """Returns a list of users """

    users = get_users(username)
    response = {}
    for user in users:
        response[str(user)] = {"methods": ast.literal_eval(user.methods)}

    return response


def get_users_keys(username):
    users = get_user(username)
    print(users)


def requires_apikey(function):
    """Decorator to validate the API Keys """
    @wraps(function)
    def decorated_function(*args, **kwargs):

        users = get_users()
        #if request.args.get('key') and request.args.get('key') == key:
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
return decorated_function
