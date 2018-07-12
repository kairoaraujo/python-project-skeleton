#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
from functools import wraps
from flask import request, jsonify
from project_name.apiusers import get_apiusers_method_keys


def std_response(state, message):
    """Returns a standard dict response """

    response = {
        "status": state,
        "message": message
    }

    return response


def requires_apikey(function):
    """Decorator to validate the API Keys """
    @wraps(function)
    def decorated_function(*args, **kwargs):

        # request
        apikey = request.headers.get("x-api-key")
        username = request.headers.get("username")
        method = str(request.method)

        # database
        db_apiuser = get_apiusers_method_keys(username)
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
                response.status_code = 403

                return response

            else:

                function_result = function(*args, **kwargs)

                return function_result

        else:

                response = jsonify(
                    std_response(False, "Not Authorized")
                )
                response.status_code = 403

                return response

    return decorated_function
