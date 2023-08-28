#!/usr/bin/python3
"""User route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.state import State
from models.user import User
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_get(city_id):
    """Return json file the dicionary of all places"""
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    lis = []
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            lis.append(place.to_dict())
    return jsonify(lis)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def places_get_with_id(place_id):
    """Return json file the dicionary of an object by its id"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def places_post(city_id):
    """Returns json file the dicionary of a new added object"""
    obj_state = storage.get(City, city_id)
    if obj_state is None:
        abort(404)
    response = request.get_json()
    if response is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in response:
        return jsonify({"error": "Missing user_id"}), 400
    elif storage.get(User, response['user_id']) is None:
        abort(404)
    elif 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_place = Place(**response, city_id=city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Search for places"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif len(data) == 0 or all(len(v) == 0 for v in data.values()):
        return jsonify([obj.to_dict() for obj in storage.all(Place).values()])

    show = None
    if data.get("cities") and len(data.get("cities")) > 0:
        cities = data["cities"]
        show = [v for v in storage.all(Place).values() if v.city_id in cities]
    if data.get("states") and len(data["states"]) > 0:
        states = data["states"]
        if show:
            cities = [v.id for v in storage.all(
                City).values() if v.state_id in states]
            show = [place
                    for place in storage.all(Place).values()
                    if place.city_id in cities and place.id
                    not in [v.id for v in show]] + show
        else:
            cities = [v.id for v in storage.all(
                City).values() if v.state_id in states]
            show = [v for v in storage.all(
                Place).values() if v.city_id in cities]
    flag = 0  # flag to check if amenities exist
    new_list_places = []
    if data.get("amenities") and len(data.get("amenities")) > 0:
        flag = 1
        if show:
            for value in show:
                exist = []
                for id in data["amenities"]:
                    if id in [v.id for v in value.amenities]:
                        exist.append(True)
                    else:
                        exist.append(False)
                if all(exist):
                    new_list_places.append(value)
        else:
            for value in storage.all(Place).values():
                exist = []
                for id in data["amenities"]:
                    if id in [v.id for v in value.amenities]:
                        exist.append(True)
                    else:
                        exist.append(False)
                if all(exist):
                    new_list_places.append(value)
        all_places = [v.to_dict() for v in new_list_places]
        for place in all_places:
            amenities = place["amenities"]
            place["amenities"] = [amen.to_dict() for amen in amenities]
    if flag:
        return jsonify(all_places)
    else:
        return jsonify([v.to_dict() for v in show])


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def places_delete(place_id):
    """returns a json file with an empty dictionary if succes del"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def places_put(place_id):
    """returns a json file with the dictionary"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    for k, v in data.items():
        if k not in ignore:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
