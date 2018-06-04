#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from project_name import version
from flask_restplus import Namespace, Resource
from flask import Flask, jsonify

app = Flask(__name__)
ns = Namespace('project', description='project description')


@ns.route('/version')
class Version(Resource):
    def get(self):
        """API version """
        output = {
            'component-name': 'project',
            'version': version
        }

        return jsonify(output)
