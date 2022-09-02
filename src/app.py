from flask import Flask
from flask import jsonify
from flask import request
from flask import json

app = Flask(__name__)




@app.route('/people', methods=['GET'])
def returnPeople():
    return jsonify(people)

@app.route('/people/<int:people_id>', methods=['POST'])
def addPeople(people_id):
    return jsonify(people)

@app.route('/people/<int:people_id>', methods=['PUT'])
def updatePeople(people_id):
    return jsonify(people)

@app.route('/people/<int:people_id>', methods=['DELETE'])
def deletePeople(people_id):
    return jsonify(people)

@app.route('/people/<int:people_id>', methods=['GET'])
def returnPerson(people_id):
    return jsonify(people[people_id])

@app.route('/planets', methods=['GET'])
def returnPlanets():
    return jsonify(planets)

@app.route('/planets/<int:planet_id>', methods=['POST'])
def addPlanet(planet_id):
    return jsonify(people[planet_id])

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def updatePlanet(planet_id):
    return jsonify(people[planet_id])

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def deletePlanet(planet_id):
    return jsonify(people[planet_id])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def returnPlanet(planet_id):
    return jsonify(people[planet_id])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def returnPlanet(planet_id):
    return jsonify(people[planet_id])

@app.route('/users', methods=['GET'])
def returnUsers():
    return jsonify(users)

@app.route('/users/favorites', methods=['GET'])
def returnUserFavorites():
    return jsonify(user.favorites)

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def addUserPlanetFavorite():
    
    return jsonify(user.favorites)

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def addUserPeopleFavorite():
    
    return jsonify(user.favorites)

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def removeUserPlanetFavorite():
    
    return jsonify(user.favorites)

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def removeUserPeopleFavorite():
    
    return jsonify(user.favorites)
