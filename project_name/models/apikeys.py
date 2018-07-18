#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: kairo@kairo.eti.br
#
from project_name import db


class APIKeys(db.Model):

    __tablename__ = "apikeys"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    apikey = db.Column(db.String(256), index=True, unique=True)
    enable = db.Column(db.Boolean, default=False, nullable=False)
    methods = db.Column(db.String(128), index=True)

    def __init__(self, username, apikey, enable, methods):
        self.username = username
        self.apikey = apikey
        self.state = enable
        self.methods = methods

    def __repr__(self):
        return self.username
