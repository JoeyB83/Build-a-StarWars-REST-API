from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Favorite_Characters = db.Table(
    "Favorite_Characters",    
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("characters_id", db.Integer, db.ForeignKey("characters.id"), primary_key=True),
)

Favorite_Planets = db.Table(
    "Favorite_Planets",    
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("characters_id", db.Integer, db.ForeignKey("planets.id"), primary_key=True),
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favCharacters = db.relationship(
        "Characters", secondary=Favorite_Characters, backref="userFavCharacters"
    )
    favPlanets = db.relationship(
        "Planets", secondary=Favorite_Planets, backref="userFavPlanets"
    )
    # favorite_characters = db.relationship("Favorite_Characters", lazy=True)
    # favorite_planets = db.relationship("Favorite_Planets")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favCharacters": self.favCharacters
            # do not serialize the password, its a security breach
        }

    # def serialize_with_favorites(self):
    #     favorite_characters = [user_fav_characters.serialize() for user_fav_characters in self.favorite_characters]
    #     favorite_planets = [user_fav_planets.serialize() for user_fav_planets in self.favorite_planets]
    #     return {
    #         "id": self.id,
    #         "email": self.email,
    #         "lista_favoritos": favorite_characters+favorite_planets
    #     }    

class Characters(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    birth_year = db.Column(db.String(100), unique=False, nullable=False)
    gender = db.Column(db.String(100), unique=False, nullable=False)
    hair_color = db.Column(db.String(100), unique=False, nullable=False)
    eye_color = db.Column(db.String(100), unique=False, nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(100), unique=False, nullable=False)    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain
       }

# class Favorite_Characters(db.Model):      
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), primary_key=True)
#     user_fav_characters = db.relationship("Characters")

#     def serialize(self):
#         return{
#             "id" : id.self,
#             "user_id" : user_id.self,
#             "character_id" : character_id.self            
#         }

# class Favorite_Planets(db.Model):      
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), primary_key=True)
#     user_fav_planets = db.relationship("Planets")

#     def serialize(self):
#         return{
#             "id" : id.self,
#             "user_id" : user_id.self,
#             "planet_id" : planet_id.self
#         }                                               