#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import environ
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')

@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                    strict_slashes=False)
def get_amenities(place_id):
    """ get amenities for a place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if STORAGE_TYPE == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get("Amenity", amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                    methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """ delete an amenity from a place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if STORAGE_TYPE == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    place.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                    methods=['POST'], strict_slashes=False)
def post_amenity(place_id, amenity_id):
    """ add an amenity to a place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if STORAGE_TYPE == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict())
        place.amenity_ids.append(amenity_id)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
