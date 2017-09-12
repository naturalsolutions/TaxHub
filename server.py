#coding: utf8
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import importlib
import datetime

db = SQLAlchemy()
app_globals = {}


class ReverseProxied(object):

    def __init__(self, app, script_name=None, scheme=None, server=None):
        self.app = app
        self.script_name = script_name
        self.scheme = scheme
        self.server = server

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '') or self.script_name
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        scheme = environ.get('HTTP_X_SCHEME', '') or self.scheme
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        server = environ.get('HTTP_X_FORWARDED_SERVER', '') or self.server
        if server:
            environ['HTTP_HOST'] = server
        return self.app(environ, start_response)

def init_app():
    if app_globals.get('app', False):
        app = app_globals['app']
    else :
        app = Flask(__name__)

    app.config.from_pyfile('config.py')
    db.init_app(app)
    # from werkzeug.contrib.fixers import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app) #
    app.wsgi_app = ReverseProxied(app.wsgi_app, script_name='/taxhub')

    from apptax.index import routes
    app.register_blueprint(routes, url_prefix='/')

    from pypnusershub import routes
    app.register_blueprint(routes.routes, url_prefix='/api/auth')

    from apptax.taxonomie.routesbibnoms import adresses
    app.register_blueprint(adresses, url_prefix='/api/bibnoms')

    from apptax.taxonomie.routestaxref import adresses
    app.register_blueprint(adresses, url_prefix='/api/taxref')

    from apptax.taxonomie.routesbibattributs import adresses
    app.register_blueprint(adresses, url_prefix='/api/bibattributs')

    from apptax.taxonomie.routesbiblistes import adresses
    app.register_blueprint(adresses, url_prefix='/api/biblistes')

    from apptax.taxonomie.routestmedias import adresses
    app.register_blueprint(adresses, url_prefix='/api/tmedias')

    from apptax.taxonomie.routesbibtypesmedia import adresses
    app.register_blueprint(adresses, url_prefix='/api/bibtypesmedia')

    from apptax.admin.admin import setup_admin
    setup_admin(app)

    return app
app = init_app()
CORS(app)
if __name__ == '__main__':
    app.run()
