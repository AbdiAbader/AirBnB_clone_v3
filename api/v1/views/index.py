#!/usr/bin/python3
from api.v1.views import app_views as app
from flask import jsonify



@app.route('/status', strict_slashes=False)
def status():
    """Returns a JSON: status: OK"""
    return jsonify({"status": "OK"})
