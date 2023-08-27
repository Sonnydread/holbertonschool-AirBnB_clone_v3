#!/usr/bin/python3
"""State"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Return json file the dictionary of all states"""
    lis = []
    for i in storage.all(State).values():
        lis.append(i.to_dict())

    return jsonify(lis)


@app_views.route('/states/<s_id>', methods=['GET'], strict_slashes=False)
def states_id(s_id):
    """Return json file the dictionary of an object by its id"""
    obj = storage.get(State, s_id)
    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post():
    """Return json file the dictionary of a newly added object"""
    response = request.get_json()

    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in response:
        return jsonify({'error': 'Missing name'}), 400

    state = State(name=response['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<s_id>', methods=['DELETE'], strict_slashes=False)
def states_delete(s_id):
    """Return json file with an empty dictionary if successfully deleted"""
    objc = storage.get(State, s_id)

    if objc is None:
        abort(404)

    storage.delete(objc)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<s_id>', methods=['PUT'], strict_slashes=False)
def states_put(s_id):
    """Return json file with the dictionary of an object updated"""
    objc = storage.get(State, s_id)

    if objc is None:
        abort(404)

    response = request.get_json()
    if response is None:
        return jsonify({'error': 'not a json'}), 400
    data = ['id', 'created_at', 'updated_at']

    for key, value in response.items():
        if key not in data:
            setattr(objc, key, value)

    storage.save()
    return jsonify(objc.to_dict()), 200
