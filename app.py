#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from flask_restplus import Api
from project_name import app
from project_name import db
from project_name import version
from project_name.models import apikeys
from project_name.api.v1.project import ns as ns_method
import logging
import os

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
    title="Project Name API",
    description="A Project description of API",
)


api.add_namespace(ns_method, path="/api/project")

"""
def bootstrap():
    username = os.environ["BOOTSTRAP_USER"]
    apikey = os.environ["BOOTSTRAP_KEY"]
    logging.info(f"Bootstrap User:{username}, Apikey: {apikey}")
    bootstrap = apikeys.BootStrap(username, apikey, 0)
    db.session.add(bootstrap)
    db.session.commit()
    logging.info("Bootstrap completed.")


tables = []
for table in db.metadata.sorted_tables:
    if "bootstrap" == table.name:
        bootstrap()

"""
