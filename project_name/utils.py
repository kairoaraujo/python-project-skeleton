#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
from functools import wraps
from flask import request, jsonify
from project_name.apiusers import get_methods_keys
from project_name import bootstrap


def std_response(state, message):
    """Returns a standard dict response """

    response = {
        "status": state,
        "message": message
    }

    return response


def requires_apikey(function_wrap):
    """Decorator to validate the API Keys """
    @wraps(function_wrap)
    def decorated_function(*args, **kwargs):

        if bootstrap.status():
            response = jsonify(
                std_response(False, "System without bootstrap.")
            )
            response.status_code = 500

            return response

        # request
        apikey = request.headers.get("x-api-key")
        username = request.headers.get("username")
        if apikey is None or username is None:
            response = jsonify(
                std_response(
                    False, "'x-api-key' and 'username' are required."
                )
            )
            response.status_code = 501

            return response

        method = str(request.method)

        # database

        db_apiuser = get_methods_keys(username)
        if (
            username and
            username in db_apiuser.keys() and
            apikey and
            apikey == db_apiuser[username]['apikey']
        ):
            if method not in db_apiuser[username]['methods']:

                response = jsonify(
                    std_response(False, "Forbidden")
                )
                response.status_code = 401

                return response

            else:

                function_result = function_wrap(*args, **kwargs)

                return function_result

        else:

                response = jsonify(
                    std_response(False, "Not Authorized")
                )
                response.status_code = 403

                return response

    return decorated_function
