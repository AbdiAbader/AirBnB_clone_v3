#!/usr/bin/python3
""" index file """


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    '''
        return status of API
    '''
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def storage_counts():
    """ returns the number of each objects by type """
    count = {}
    count["amenities"] = storage.count("Amenity")
    count["cities"] = storage.count("City")
    count["places"] = storage.count("Place")
    count["reviews"] = storage.count("Review")
    count["states"] = storage.count("State")
    count["users"] = storage.count("User")
    return jsonify(count)
