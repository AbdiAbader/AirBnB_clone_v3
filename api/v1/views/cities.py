#!/usr/bin/python3


""" cities routes """


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ Retrieves the list of all City objects """
    state = storage.get('State', state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities], strict_slashes=False)
    else:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object """
    city = storage.get('City', city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """Deletes city by city_id"""
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        return jsonify({})
    else:
        abort(404)

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a City object"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, k, v)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
