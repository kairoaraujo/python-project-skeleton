#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))
DATABASE = os.path.join(
    PROJECT_ROOT, "project_name", "databases", "project_name.db")
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE
SQLALCHEMY_TRACK_MODIFICATIONS = False
