from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active" : self.is_active
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(100), unique=False, nullable=False)
    hair_color = db.Column(db.String(100), unique=False, nullable=False)
    eye_color = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return f'<People id ={self.id}, name= {self.name}, gender={self.gender},hair_color = {self.hair_color}, eye_color = {self.eye_color}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color            
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.String(120), unique=False, nullable=False)
    terrain = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Planet id={self.id}, name={self.name}, population ={self.population}, terrain={self.terrain}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain            
        }

class PeopleFavorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=True, nullable=False)
    peopleId = db.Column(db.Integer, unique=False, nullable=False)
    

    def __repr__(self):
        return f'<PeopleFavorite id ={self.id}, userId ={self.userId}, peopleId ={self.peopleId}>'

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "peopleId": self.peopleId                       
        }

class PlanetFavorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=True, nullable=False)
    planetId = db.Column(db.Integer, unique=False, nullable=False)
    

    def __repr__(self):
        return f'<PeopleFavorite id ={self.id}, userId ={self.userId}, planetId ={self.planetId}>'

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "planetId": self.planetId                       
        }