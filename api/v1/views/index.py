#!/usr/bin/python3
"""New route"""
from flask import Flask, jsonify
from . import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """Return the status of our api"""
    dic = {'status': 'OK'}
    return jsonify(dic)


@app_views.route('/stats', methods=['GET'])
def stats():
    """Return the number of objects"""
    d = {"amenities": storage.count(Amenity),
         "cities": storage.count(City),
         "places": storage.count(Place),
         "reviews": storage.count(Review),
         "states": storage.count(State),
         "users": storage.count(User)}
    return jsonify(d)
