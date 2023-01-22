#!/usr/bin/python3
"""This module contains the Flask app"""
from flask import Flask, jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def tear_down(self):
    '''
    close query after each session
    '''
    storage.close()


if __name__ == "__main__":
    app.register_blueprint(app_views)
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', 5000), threaded=True))
