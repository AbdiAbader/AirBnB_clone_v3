#!/usr/bin/python3
"""places amenities"""


from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                    strict_slashes=False)
def place_amenity(place_id):
    """ Retrieves the list of all Amenity objects  of a Place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                    methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """ Deletes a Amenity object to a Place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({})


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                    methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """ Creates a Amenity object to a Place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


if __name__ == "__main__":
    pass
