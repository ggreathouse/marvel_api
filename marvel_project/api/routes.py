from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from marvel_project.helpers import token_required
from marvel_project.models import db, User, Character, character_schema, characters_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value'}

#Create Character Endpoint    Might need to add date_created
@api.route('/characters', methods = ['POST'])
@token_required
def create_character(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    preferred_weapon = request.json['preferred_weapon']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    character = Character(name, description, comics_appeared_in, super_power, preferred_weapon, user_token=user_token)

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)


# Retrieve all Character Endpoint
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token = owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)


#Retrieve one character endpoint
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


#Update Superhero Endpoint
@api.route('/characters/<id>', methods = ['POST', 'PUT'])
@token_required
def update_superhero(current_user_token, id):
    character = Character.query.get(id)

    character.name = request.json['name']
    character.description = request.json['description']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.super_power = request.json['super_power']
    character.preferred_weapon = request.json['preferred_weapon']
    character.user_token = current_user_token.token

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)

#Delete Character Endpoint
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_id, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)