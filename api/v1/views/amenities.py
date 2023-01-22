#!/usr/bin/python3
""" Amenity objects that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities = storage.all('Amenity')
    return jsonify([amenity.to_dict() for amenity in amenities.values()])

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an Amenity object """
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """Deletes amenity by amenity_id"""
    amenity = storage.delete('Amenity', amenity_id)
    if amenity:
        return jsonify(amenity_id.to_dict())
    else:
        abort(400)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates an Amenity"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Updates an Amenity"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())
    else:
        abort(404)
