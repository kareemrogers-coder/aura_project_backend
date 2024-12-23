import jwt
import os
from datetime import datetime, timedelta, timezone
from  functools import wraps
from flask import request, jsonify
import config


SECRET_KEY = os.environ.get('SECRET_KEY') #THIS IS BEING PULL FROM .ENV.


def token_generator(email):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'email': email,
        'exp': expiration_time
    }
    secret_key = config('SERCET_KEY')
    return jwt.encode(payload, secret_key, algorithm= 'HS256')


#TOKEN CREATION 
def encode_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days= 0, hours = 2),
        'iat': datetime.now(timezone.utc), 
        'sub': user_id
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split()[1]
                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print("PAYLOAD:", payload)       
            except jwt.ExpiredSignatureError:
                return jsonify({'message': "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid Token"}), 401  

            return func(*args, **kwargs)
        else:
            return jsonify({"messages": "Token Authorization required"}), 401
        
    return wrapper