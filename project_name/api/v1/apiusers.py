#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from flask_restplus import Namespace, Resource
from flask import request
from project_name.apiusers import get_apiusers_methods, add_apiuser
from project_name.utils import requires_apikey


ns = Namespace("apiusers", description="API Users configuration managment")


@ns.route("/apiuser")
class Users(Resource):

    @requires_apikey
    def get(self):
        """GET all users and methods allowed to them.

        Returns:

            {
                'username': [methods_list]
            }
        """
        response = get_apiusers_methods()

        return response


@ns.route("/apiuser/<username>")
class Usersname(Resource):

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
        response = get_apiusers_methods(username)

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

        response = add_apiuser(payload)

        return response


@ns.route("/apiuser/apikey/<username>")
class Usersname(Resource):

    @requires_apikey
    def get(self, username):
        """GET information for a specific user.

        Returns:

            {
            'username': {
                methods: [methods_list],
                apikey: 'api key hash'
            }
        """
        print(username)
        response = get_apiusers_methods(username)

        return response


