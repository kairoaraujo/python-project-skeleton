#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from flask_restplus import Namespace, Resource
from flask import jsonify, request
from project_name.utils import get_users
from project_name.utils import std_response


ns = Namespace("users", description="User configuration managment")


@ns.route("/users")
class Users(Resource):
    def get(self):
        """GET users list

        Returns:
            {
                "username": methods_list
        """
        response = jsonify(get_users())
        response.status_code = 200

        return response

    def post(self):
        """POST Bootstrap configuration

        It generates the first user / api keys user and after that
        Bootstrap is disabled.

        Payload required: JSON format

        keys:
            - "username": The username
            - "methods": ["ALL"] Recommended for bootstrap

        Sample:

            {
                "username": "appadmin",
                "methods": ["ALL"]
            }

        Response:

            {
                "username": "appadmin",
                "apikey": "apikey hash",
                "methods": ["GET", "POST", "PUT", "DELETE"]
            }
        """
        payload = request.get_json(force=True)

        response = execute(payload)
        if "status" in response:
            response = jsonify(response)
            response.status_code = 400

        else:
            response = jsonify(response)
            response.status_code = 200

        return response

