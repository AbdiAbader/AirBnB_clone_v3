#!/usr/bin/python3

"""This module contains the Flask app"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON status"""
    return jsonify({'status': 'OK'})