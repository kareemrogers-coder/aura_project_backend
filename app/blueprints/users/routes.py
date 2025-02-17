from flask import request, jsonify, Flask
from app.blueprints.users import users_bp
from .schemas import user_schema,login_schema,users_schema
from marshmallow import ValidationError
from app.models import Users, db, OAuth
from sqlalchemy import select
from app.extensions import limiter
from app.utils.util import token_required, verify_token, encode_token, token_generator
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
import re

def token_generator(email):
    return create_access_token(identity=email)

def pwd_validation(password):
    if len(password) < 8:
        return "Password should be at least 8 character long."
    if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
        return "Password should contain both letters and numbers."
    return None



# Login user v3

@users_bp.route("/login", methods=['POST'])
# @token_required
def login():
    # print(payload)
    # verify if the request from the frontend contains a Oauth token

    info = request.get_json()

    google_login = info.get('google_login')
    google_token = info.get('google_token')
    auth0_token = info.get('auth0_token')



    if google_login and google_token:
        google = OAuth.create_client('google')
        try:
            token = google.authorize_access_token()
            user_info = google.parse_id_token(token)

            email = user_info['email']
            name = user_info['name']

            user = Users.query.filter_by(email=email).first()

            #if user exist 
            if user:
                #access_token = token_generator(email)
                access_token = create_access_token(identity='user1')
                return jsonify({'access_token': access_token, 'user_info': {'email': email, 'name': name}}), 200
            else:
                new_google_user = Users(email=email, name=name, password=None)
                db.session.add(new_google_user)
                db.session.commit()

                access_token = token_generator(email)

                return jsonify({
                    'message': "token generated successfully",
                    'access_token': access_token,
                    'user_info': {'email': email, 'name': name}}), 201

        except Exception as e:
            return jsonify({"message": "Invalid Google Token",}), 400

    if auth0_token:
        try:
            payload = verify_token(auth0_token)

            email = payload['email']
            name = payload['name']

            #user = Users.query.filter_by(email=email).first()
            user =db.session.query(Users).filter_by(email=email).first()
            if user:
                # access_token = token_generator(email)
                access_token = create_access_token(identity='user1')
                return jsonify({ 'access_token': access_token, 'user_info': {'email': email, 'name': name}}), 200
            else:
                new_user = Users(email=email, name=name, password=None)
                db.session.add(new_user)
                db.session.commit()
                access_token = token_generator(email)

                return jsonify({
                    'message': "Token generated successfully",
                    'access_token': access_token,
                    'user_info': {'email': email, 'name': name}
                }), 201
        except ValidationError as e:
            return jsonify({"message": str(e)}), 400
        
       #Validate the payload and ensure they sent us email and password   
    try:
        creds = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Users).where(Users.email == creds['email'])
    user = db.session.execute(query).scalars().first()


    if user and check_password_hash(user.password, creds['password']): #If a user exist within the database, with the same email password combination

            token = encode_token(user.id)

            response = {
                "message": "successfully logged in",
                "status": "success",
                "token": token
            }
        
            return jsonify(response), 200
        
        
    return jsonify({"message": "Invalid email or password!"}), 400



@users_bp.route("/sign-up", methods=['POST'])
# @limiter.limit("3 per hour")
def create_user():
    #Validate and Deserialize incoming data
    try:
        user_data = user_schema.load(request.json)
    #If data invalid respond with error message
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #check for password validatiin 
    pwd_error = pwd_validation(user_data['password'])
    if pwd_error:
        return jsonify({"message": pwd_error}), 400
    
    query = select(Users).where(Users.email == user_data['email'])
    existing = db.session.execute(query).scalars().first()
    if existing:
        return jsonify({"message": "Account already associated with that email."}), 400
    
    #If data is valid, create new user with that data
    pwhash = generate_password_hash(user_data['password'])
    new_user = Users(name=user_data['name'], email=user_data['email'], password=pwhash) ## take out and DOB

    db.session.add(new_user) #Add to session
    db.session.commit() #commit session to db

    return user_schema.jsonify(new_user), 201 #return new user object as a response



@users_bp.route("/", methods=["GET"])
def get_users():
    query = select(Users)
    users = db.session.execute(query).scalars().all()

    return users_schema.jsonify(users), 200


@users_bp.route("/<int:user_id>", methods=['GET'])
def get_user(user_id):
    member = db.session.get(Users, user_id)

    return user_schema.jsonify(member), 200
