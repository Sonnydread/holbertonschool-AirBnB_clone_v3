#!/usr/bin/python3
"""City"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<s_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(s_id):
    """Return json file the dictionary of all states"""
    obj = storage.get(State, s_id)

    if obj is None:
        abort(404)

    lis_city = []
    for city in storage.all(City).values():
        if city.state_id == s_id:
            lis_city.append(city.to_dict())

    return jsonify(lis_city)


@app_views.route('/cities/<c_id>', methods=['GET'],
                 strict_slashes=False)
def cities_id(c_id):
    """Return json file the dictionary of an object by its id"""
    obj = storage.get(City, c_id)
    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route('/states/<s_id>/cities', methods=['POST'],
                 strict_slashes=False)
def cities_post(s_id):
    """Return json file the dictionary of a newly object"""
    state = storage.get(State, s_id)

    if state is None:
        abort(404)

    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in response:
        return jsonify({'error': 'Missing name'}), 400

    city = City(name=response['name'], state_id=s_id)
    storage.new(city)
    storage.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<c_id>', methods=['DELETE'],
                 strict_slashes=False)
def cities_delete(c_id):
    """Return json file the dictionary if a successfully deleted"""
    obj = storage.get(City, c_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<c_id>', methods=['PUT'],
                 strict_slashes=False)
def cities_put(c_id):
    """Return json file the dictionary of an object that updated"""
    obj = storage.get(City, c_id)
    if obj is None:
        abort(404)

    response = request.get_json()
    if response is None:
        return jsonify({'error': 'not a json'}), 400

    data = ['id', 'created_at', 'updated_at', 'state_id']
    for key, value in response.items():
        if key not in data:
            setattr(obj, key, value)

    storage.save()
    return jsonify(obj.to_dict()), 200
