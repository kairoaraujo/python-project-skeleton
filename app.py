#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# If Flask API for example
from flask import Flask
from flask_restplus import Api
from project_name import version
from project_name.api.v1.project import ns as ns_method
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

app = Flask(__name__)
api = Api(
    app,
    version=version,
    title="Project Name API",
    description="A Project description of API",
)


api.add_namespace(ns_method, path="/api/project")
