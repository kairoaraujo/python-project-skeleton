#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from flask_restplus import Api
from project_name import app
from project_name import version
from project_name.api.v1.bootstrap import ns as ns_bootstrap
from project_name.api.v1.apiusers import ns as ns_apiusers
from project_name.api.v1.jwt_calls import ns as ns_jwt_calls
from flask_restplus import Namespace, Resource
from flask import jsonify
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)

api = Api(
    app,
    version=version,
    title="project_name API",
    description="A Project description of API",
)


ns_default = Namespace("default", description="project_name main")


@ns_default.route("/version")
class Version(Resource):
    def get(self):
        """API version """
        output = {"component-name": "project_name", "version": version}

        return jsonify(output)


api.add_namespace(ns_default, path="/api/v1")
api.add_namespace(ns_bootstrap, path="/api/v1/configuration")
api.add_namespace(ns_apiusers, path="/api/v1/configuration")
api.add_namespace(ns_jwt_calls, path="/api/v1/calls")
