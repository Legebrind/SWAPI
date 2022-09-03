"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, PeopleFavorite, PlanetFavorite
import requests
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def returnUsers():
    user_query = User.query.all()
    user_query =[pokemon.serialize() for pokemon in user_query]
    return jsonify(user_query)

@app.route('/populate', methods=['GET'])
def populate():
    results = requests.get("https://swapi.dev/api/people")
    results = results.json()
    results = results["results"]
    for i in range(0,len(results)):
        person = People(
            id = i+1,
            name = results[i]["name"],
            gender = results[i]["gender"],
            hair_color = results[i]["hair_color"],
            eye_color = results[i]["eye_color"]
        )
        
        db.session.add(person)
        db.session.commit()
    
    results = requests.get("https://swapi.dev/api/planets")
    results = results.json()
    results = results["results"]
    for i in range(0,len(results)):
        planet = Planet(
            id = i+1,
            name = results[i]["name"],
            population = results[i]["population"],
            terrain = results[i]["terrain"]
        )
        db.session.add(planet)
        db.session.commit()
    
    response_body = {
        "msg": "Database has been populated "
    }
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def returnPeople():
    people_query = People.query.all()
    people_query =[i.serialize() for i in people_query]
    return jsonify(people_query), 200

@app.route('/people/<int:people_id>', methods=['POST'])
def addPeople(people_id):
    person = People.query.get(person_id)
    if person is not None:
        raise APIException('Person already exists', status_code=404)
    
    person = request.get_json()
    person = People(
            id = i+1,
            name = results[i]["name"],
            gender = results[i]["gender"],
            hair_color = results[i]["hair_color"],
            eye_color = results[i]["eye_color"]
        )
    db.session.add(person)
    db.session.commit()
    return jsonify(people), 200

@app.route('/people/<int:people_id>', methods=['PUT'])
def updatePeople(people_id):
    person = Person.query.get(person_id)
    if person is None:
        raise APIException('Person not found', status_code=404)

    if "id" in body:
        person.id = body["id"]
    if "eye_color" in body:
        person.eye_color = body["eye_color"]
    if "gender" in body:
        person.gender = body["gender"]
    if "hair_color" in body:
        person.hair_color = body["hair_color"]
    if "name" in body:
        person.name = body["name"]
    db.session.commit()
    return jsonify(person), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def deletePeople(people_id):
    person = People.query.get(person_id)
    if person is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(person)
    db.session.commit()
    return jsonify(people),200

@app.route('/people/<int:people_id>', methods=['GET'])
def returnPerson(people_id):
    person = People.query.get(people_id)
    person = person.serialize()
    return jsonify(person), 200

@app.route('/planets', methods=['GET'])
def returnPlanets():
    planet_query = Planet.query.all()
    planet_query =[pokemon.serialize() for pokemon in planet_query]
    return jsonify(planet_query), 200

@app.route('/planets/<int:planet_id>', methods=['POST'])
def addPlanet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is not None:
        raise APIException('Planet already exists', status_code=404)
    
    planet = request.get_json()
    planet = Planet(
        id = i+1,
        name = results[i]["name"],
        population = results[i]["population"],
        terrain = results[i]["terrain"]
        )
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet), 200

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def updatePlanet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)

    if "id" in body:
        planet.id = body["id"]
    if "population" in body:
        planet.population = body["population"]
    if "terrain" in body:
        planet.terrain = body["terrain"]
    if "name" in body:
        planet.name = body["name"]
    db.session.commit()
    return jsonify(planet), 200
    

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def deletePlanet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    db.session.delete(planet)
    db.session.commit()
    return jsonify(planet)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def returnPlanet(planet_id):
    planet = Planet.query.get(planet_id)
    planet = planet.serialize()
    return jsonify(planet)

@app.route('/favorites', methods=['GET'])
def returnUserFavorites():
    favoritePeople = ""
    favoritePlanet = ""
    activeUser = User.query.filter(User.is_active==True).first()
    activeUser = activeUser.serialize()
    if PeopleFavorite.query.filter(PeopleFavorite.userId == activeUser["id"]).first():
        favoritePeople = PeopleFavorite.query.filter(PeopleFavorite.userId == activeUser["id"]).all()
        favoritePeople =[pokemon.serialize() for pokemon in favoritePeople]
    if PlanetFavorite.query.filter(PlanetFavorite.userId == activeUser["id"]).first():
        favoritePlanet = PlanetFavorite.query.filter(PlanetFavorite.userId == activeUser["id"]).all()
        favoritePlanet =[pokemon.serialize() for pokemon in favoritePlanet]    
    
    return [jsonify(favoritePeople),jsonify(favoritePlanet)]
    

@app.route('/favoritePlanet/<int:planet_id>', methods=['POST'])
def addUserPlanetFavorite(planet_id):
    activeUser = User.query.filter(User.is_active==True).first()
    if PlanetFavorite.query.filter(PlanetFavorite.userId == activeUser.id and planet_id == PlanetFavorite.planetId).first() is not None:
        addPlanet = PlanetFavorite(
           id = PlanetFavorite.query.count()+1,
           userId = activeUser.id,
           planetId = planet_id
        )
        db.session.add(addPlanet)
        db.session.commit()
    response_body = {
        "msg" : "Planet added"
    }
    return jsonify(response_body)

@app.route('/favoritePeople/<int:people_id>', methods=['POST'])
def addUserPeopleFavorite():
    activeUser = User.query.filter(User.is_active==True).first()
    if PeopleFavorite.query.filter(PeopleFavorite.userId == activeUser.id and people_id == PeopleFavorite.peopleId).first() is not None:
        addPeople = PeopleFavorite(
           id = PeopleFavorite.query.count()+1,
           userId = activeUser.id,
           peopleId = people_id
        )
        db.session.add(addPeople)
        db.session.commit()
    response_body = {
        "msg" : "Person added"
    }
    return jsonify(body_message)

@app.route('/favoritePlanet/<int:planet_id>', methods=['DELETE'])
def removeUserPlanetFavorite():
    activeUser = User.query.filter(User.is_active==True).first()
    return jsonify(user.favorites)

@app.route('/favoritePeople/<int:people_id>', methods=['DELETE'])
def removeUserPeopleFavorite():
    activeUser = User.query.filter(User.is_active==True).first()
    return jsonify(user.favorites)


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
