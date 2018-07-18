#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from flask_restplus import Namespace, Resource
from flask import request
from project_name import apiusers
from project_name.utils import requires_apikey


ns = Namespace("apiusers", description="API Users configuration management")


@ns.route("/apiusers")
class Users(Resource):

    @requires_apikey
    def get(self):
        """GET all users and methods allowed to them.

        Returns:

            {
                'username': [methods_list]
            }
        """
        response = apiusers.get_methods()

        return response

    @requires_apikey
    def post(self):
        """POST creates a new user with the methods.
                Payload required: JSON format

        keys:
            - "username": user name
            - "methods": list of allowed methods (GET, POST, PUT, DELETE)

        Sample:

            {
                "username": "app1",
                "methods": ["GET", "POST"]
            }

        Response:

            {
                "username": "app1",
                "apikey": "apikey hash",
                "methods": ["GET", "POST"]
            }
        """
        payload = request.get_json(force=True)

        response = apiusers.add(payload)

        return response


@ns.route("/apiusers/<username>")
class Username(Resource):

    @requires_apikey
    def get(self, username):
        """GET information for a specific user.

        Returns:

            {
                'username1': [methods_list],
                'username2': [methods_list],
                ...
            }
        """
        response = apiusers.get_methods(username)

        return response

    @requires_apikey
    def put(self, username):
        """PUT modifies an user methods or generates a new API keys.
               Payload required: JSON format

        keys:
            - "methods": new list of allowed methods (GET, POST, PUT, DELETE)
            - "apikey": Boolean. True creates new apikey | False keep apikey

        Sample:

            {
                "methods": ["GET", "POST"]
                "apikey": True
            }

        Response:

            {
                "username": "app1",
                "apikey": "apikey hash",
                "methods": ["GET", "POST"]
            }
        """
        payload = request.get_json(force=True)

        response = apiusers.update(payload, username)

        return response
