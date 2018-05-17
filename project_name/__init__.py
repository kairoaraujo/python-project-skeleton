#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Kairo Araujo <kairo@kairo.eti.br>
#

from os.path import dirname, join

with open(join(dirname('..'), 'VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()
