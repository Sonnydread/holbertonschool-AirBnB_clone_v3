#!/usr/bin/python3
"""Amenities routs"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities():
    """Return json file the dictionary of all amenities"""
    lis = []

    for ame in storage.all(Amenity).values():
        lis.append(ame.to_dict())

    return jsonify(lis)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """Return json file with the dictionary of object its id"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def amenities_post():
    """Return json file with the dictionary of a newly object"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity = Amenity(name=data['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenities_delete(amenity_id):
    """Return json file with an empty dictionary if successfully deleted"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenities_put(amenity_id):
    """Return json file the dictionary of an object updated"""
    response = storage.get(Amenity, amenity_id)
    if response is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    res = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in res:
            setattr(response, key, value)

    storage.save()
    return jsonify(response.to_dict()), 200
