# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

CSRF_ENABLED = True
SECRET_KEY = '34pw-rjjexnd-3@^_7k$%wv1=9*4rq*mrv*mtkf2#y6@fh1wri'
