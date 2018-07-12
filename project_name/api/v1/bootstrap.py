#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from flask_restplus import Namespace, Resource
from flask import jsonify, request
from project_name.bootstrap import status, execute
from project_name.utils import std_response


ns = Namespace("bootstrap", description="Bootstrap configuration managment")


@ns.route("/bootstrap")
class Bootstrap(Resource):
    def get(self):
        """GET bootstrap configuration state"""

        if status():
            state = True
            message = "Bootstrap is available to be configured."

        else:
            state = False
            message = "Bootstrap not available. Bootstrap already done."

        return std_response(state, message)

    def post(self):
        """POST Bootstrap configuration

        It generates the first user / api keys user and after that
        Bootstrap is disabled.

        Payload required: JSON format

        keys:
            - "username": user name
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

        if not status():
            return std_response(
                False,
                "Bootstrap not available. Bootstrap already done."
            )

        response = execute(payload)
        if "status" in response:
            response = jsonify(response)
            response.status_code = 400

        else:
            response = jsonify(response)
            response.status_code = 200

        return response

