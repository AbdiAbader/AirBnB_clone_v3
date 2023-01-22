from flask import abort, Blueprint, jsonify, make_response, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects """
    return jsonify([state.to_dict() for state in storage.all('State')])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object """
    state = storage.get('State', state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """Deletes state by state_id"""
    state = storage.delete('State', state_id)
    if state:
        return jsonify(state_id.to_dict())
    else:
        abort(400)
