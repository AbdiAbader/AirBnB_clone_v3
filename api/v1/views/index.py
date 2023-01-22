#!/usr/bin/python3

"""This module contains the Flask app"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views

@app_views.route("/status")
def status():
    '''
        return JSON of OK status
    '''
    return jsonify({'status': 'OK'})