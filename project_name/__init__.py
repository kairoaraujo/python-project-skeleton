#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
from flask import Flask
from os.path import dirname, join
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from settings import DEBUG
from project_name.constants.database import SQLALCHEMY_DATABASE_URI
from project_name.constants.database import SQLALCHEMY_TRACK_MODIFICATIONS

with open(join(dirname(".."), "VERSION"), "rb") as f:
    version = f.read().decode("ascii").strip()

app = Flask(__name__)
app.config["DEBUG"] = DEBUG
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

migrate = Migrate(app, db)
