#!/usr/bin/python3
"""User route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.state import State
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Return json file the dicionary of all users"""
    lis = []
    for i in storage.all(User).values():
        lis.append(i.to_dict())

    return jsonify(lis)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users_id(user_id):
    """Return json file the dictionary of an object by its id"""
    response = storage.get(User, user_id)
    if response is None:
        abort(404)

    return jsonify(response.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users_post():
    """Return json file the dictionary of newly object"""
    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'email' not in response:
        return jsonify({'error': 'Missing email'}), 400
    elif 'password' not in response:
        return jsonify({'error': 'Missing password'}), 400

    user = User(email=response['email'], password=response['password'])
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def users_delete(user_id):
    """Return json file an empty dictionary"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def users_put(user_id):
    """Return json file the dictionary of object updated"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400

    data = ['id', 'created_at', 'updated_at', 'email']
    for key, value in response.items():
        if key not in data:
            setattr(obj, key, value)

    storage.save()
    return jsonify(obj.to_dict()), 200
