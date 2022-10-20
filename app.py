from datetime import timedelta
from sqlite3 import IntegrityError
from flask import Flask, jsonify, request
app = Flask(__name__)

from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_jwt_extended import JWTManager, create_access_token, jwt_required
jwt = JWTManager(app)

## DB CONNECTION AREA

from flask_sqlalchemy import SQLAlchemy 
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://tomato:123456@localhost:5432/ripe_tomatoes_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = 'hello'

db = SQLAlchemy(app)

# CLI COMMANDS AREA

@app.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@app.cli.command("seed")
def seed_db():

    # Added users here
    users = [
        User(
        username="Erkan",
        password=bcrypt.generate_password_hash("eggs").decode('utf-8')
        ),
        User(
        username="Oli",
        password=bcrypt.generate_password_hash("eggs2").decode('utf-8')
        )
    ]
    db.session.add_all(users)

    movie1 = Movie(
        title = "Spider-Man: No Way Home",
        genre = "Action",
        length = 148,
        year = 2021
    )
    db.session.add(movie1)

    movie2 = Movie(
        title = "Dune",
        genre = "Sci-fi",
        length = 155,
        year = 2021
    )
    db.session.add(movie2)

    actor1 = Actor(
        first_name = "Tom",
        last_name = "Holland",
        gender = "male",
        country = "UK"
    )
    db.session.add(actor1)

    actor2 = Actor(
        first_name = "Marisa",
        last_name = "Tomei",
        gender = "female",
        country = "USA"
    )
    db.session.add(actor2)

    actor3 = Actor(
        first_name = "Timothee",
        last_name = "Chalemet",
        gender = "male",
        country = "USA"
    )
    db.session.add(actor3)

    actor4 = Actor(
        first_name = "Zendaya",
        last_name = "",
        gender = "female",
        country = "USA"
    )
    db.session.add(actor4)
   
    db.session.commit()
    print("Tables seeded") 

@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 

# MODELS AREA

# made changes here first.
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)


class Movie(db.Model):
    __tablename__= "MOVIES"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String())
    genre = db.Column(db.String())
    length = db.Column(db.Integer())
    year = db.Column(db.Integer())

class Actor(db.Model):
    __tablename__= "ACTORS"
    id = db.Column(db.Integer,primary_key=True)  
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    gender = db.Column(db.String())
    country = db.Column(db.String())

# SCHEMAS AREA

class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "password")

class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "genre", "length", "year")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

class ActorSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "gender", "country")

actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)


# ROUTING AREA

@app.route("/")
def hello():
  return "Welcome to Ripe Tomatoes API"

@app.route("/movies/", methods=["GET"])
def get_movies():
    movies_list = Movie.query.all()
    result = movies_schema.dump(movies_list)
    return jsonify(result)

@app.route("/actors/", methods=["GET"])
@jwt_required()
def get_actors():
    actors_list = Actor.query.all()
    result = actors_schema.dump(actors_list)
    return jsonify(result)

@app.route('/auth/signup/', methods=['POST'])
def signup():
    try:
        # load the posted user info and parse the JSON
        user_signup = UserSchema().load(request.json)
        # Create a new user model instance from the user_info
        user = User(
            username=user_signup['username'],
            password=bcrypt.generate_password_hash(user_signup['password']).decode('utf8')
        )
        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # Respond to client
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'please enter correct password or user'}, 409

@app.route('/auth/signin/', methods=['POST'])
def signin():
    stmt = db.select(User).filter_by(username=request.json['username'])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # return UserSchema(exclude=['password']).dump(user)
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'username': user.username, 'token': token}
    else:
        return {'error': 'invalid passsword or email'}, 401 