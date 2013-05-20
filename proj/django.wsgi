#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, '/usr/lib/python2.6/site-packages/')

sys.path.insert(0, '/root/test1/test1')
sys.path.insert(0, '/root/test1')


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# ------ Ниже этой линии изменения скорее всего не нужны --------

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
