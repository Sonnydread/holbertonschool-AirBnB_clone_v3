#!/usr/bin/python3
"""Review route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_get(place_id):
    """Return json file the dictionary all places"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)

    lis = []
    for r in storage.all(Review).values():
        if r.place_id == place_id:
            lis.append(r.to_dict())

    return jsonify(lis)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def reviews_get_with_id(review_id):
    """Return json file the dictionary object its id"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def reviews_post(place_id):
    """Return json file the dictionary of newly added object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'user_id' not in response:
        return jsonify({'error': 'Missing user_id'}), 400
    elif storage.get(User, response['user_id']) is None:
        abort(404)
    elif 'text' not in response:
        return jsonify({'error': 'Missing text'}), 400

    review = Review(**response, place_id=place_id)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def reviews_delete(review_id):
    """Return json file empty dictionary deleted"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def reviews_put(review_id):
    """Return json file the dictionary updated"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400

    data = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for k, v in response.items():
        if k not in data:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
