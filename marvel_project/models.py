from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

#Adding Flask Security Passwords
from werkzeug.security import generate_password_hash, check_password_hash

#Import for Secretes Module
import secrets

#Import for Login Manager
from flask_login import LoginManager, UserMixin

#Import for flask marsmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(50), nullable = False, default = '')
    last_name = db.Column(db.String(50), nullable = False, default = '')
    username = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(150), nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref = 'owner', lazy = True)

    def __init__(self, username, first_name = '', last_name = '', password='', token=''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_token(self,length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.username} has been added to the database" 
    

class Character(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String(150))
    preferred_weapon = db.Column(db.String(50), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, comics_appeared_in, super_power, preferred_weapon, user_token, id =''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.preferred_weapon = preferred_weapon
        self.user_token = user_token

    def set_id(self):
        return str((secrets.token_urlsafe()))

    def __repr__(self):
        return f"{self.name} has been added to the database"

#Creation of api schema via marsmallow object
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'comics_appeared_in', 'super_power', 'preferred_weapon']

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)