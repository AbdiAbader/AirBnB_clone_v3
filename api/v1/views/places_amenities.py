#!/usr/bin/python3
"""places amenities"""


from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                    strict_slashes=False)
def place_amenity(place_id):
    """get place information for all places in a specified city"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                    methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes a place based on its place_id"""
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
    return (jsonify({}))


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                    methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """create a new place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    place.amenities.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """ post 
     search """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    kwargs = request.get_json()
    if 'states' not in kwargs and 'cities' not in kwargs and 'amenities' not in kwargs:
        places = storage.all("Place")
        places = [place.to_dict() for place in places.values()]
        return jsonify(places)
    places = []
    if 'states' in kwargs:
        for state_id in kwargs['states']:
            state = storage.get("State", state_id)
            if state is None:
                continue
            for city in state.cities:
                for place in city.places:
                    places.append(place)
    if 'cities' in kwargs:
        for city_id in kwargs['cities']:
            city = storage.get("City", city_id)
            if city is None:
                continue
            for place in city.places:
                places.append(place)
    if 'amenities' in kwargs:
        for amenity_id in kwargs['amenities']:
            amenity = storage.get("Amenity", amenity_id)
            if amenity is None:
                continue
            for place in places:
                if amenity not in place.amenities:
                    places.remove(place)
    places = [place.to_dict() for place in places]
    return jsonify(places)

