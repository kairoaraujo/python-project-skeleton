#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from flask_restplus import Namespace, Resource
from flask import request
from project_name.utils import requires_apikey
from project_name import jwt_client

ns = Namespace("jwt_calls", description="JWT Calls")


@ns.route("/sample_call")
class Version(Resource):

    @requires_apikey
    def post(self):
        """API version """

        payload = request.get_json(force=True)

        response = jwt_client.request(
            "DELETE",
            "https://www.mocky.io/v2/5185415ba171ea3a00704eed",
            payload=payload,
            verify=False
        )

        return response
