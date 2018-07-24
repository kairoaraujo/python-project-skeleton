#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from flask_restplus import Api
from project_name import app
from project_name import version
from project_name.api.v1.project_name import ns as ns_project_name
from project_name.api.v1.bootstrap import ns as ns_bootstrap
from project_name.api.v1.apiusers import ns as ns_apiusers

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


api.add_namespace(ns_project_name, path="/api/v1")
api.add_namespace(ns_bootstrap, path="/api/v1/configuration")
api.add_namespace(ns_apiusers, path="/api/v1/configuration")
