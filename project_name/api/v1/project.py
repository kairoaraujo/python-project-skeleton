#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from project_name import version
from flask_restplus import Namespace, Resource
from flask import jsonify

ns = Namespace('project', description='project description')


ns.route('/version')
class Version(Resource):
    def get(self):
        """API version """
        output = {
            'component-name': 'project',
            'version': version
        }

        retrun jsonify(output)
