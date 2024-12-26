import jwt
import os
from datetime import datetime, timedelta, timezone
from  functools import wraps
from flask import request, jsonify,Flask
# from flask_cors import CORS
# from jose import jwt
from urllib.request import urlopen
import json

import config


SECRET_KEY = os.environ.get('SECRET_KEY') #THIS IS BEING PULL FROM .ENV.


# def token_generator(email):
#     expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#     payload = {
#         'email': email,
#         'exp': expiration_time
#     }
#     secret_key = config('SERCET_KEY')
#     return jwt.encode(payload, secret_key, algorithm= 'HS256')


# #TOKEN CREATION 
# def encode_token(user_id):
#     payload = {
#         'exp': datetime.now(timezone.utc) + timedelta(days= 0, hours = 2),
#         'iat': datetime.now(timezone.utc), 
#         'sub': user_id
#     }

#     token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    print("Verifying token")

    print("Opening URL")
    jsonurl = urlopen(f"https://{dev-y870izsbr3wx4epg.us.auth0.com}/.well-know/jwks.json")

    print("Reading json")
    jwks = json.loads(jsonurl.read())

    print("Checking verified header")
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}

    for key in jwks ["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key ["e"],


            }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_IDENTIFIER,
                    issuer=f"https://{dev-y870izsbr3wx4epg.us.auth0.com}/",
                )
                print('PAYLOAD:', payload)
                return payload
            except jwt.ExpiredSignatureError:
                raise ValueError ("Token is expired.")
            except jwt.JWTClaimsError:
                raise ValueError("Incorrect claims. Check the audience and issuer.")
            except Exception:
                raise ValueError("unable to verify autheication token")
        raise ValueError("No matching RSA Key")
    


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

            return func(payload, *args, **kwargs)
        else:
            return jsonify({"messages": "Token Authorization required"}), 401
        
    return wrapper

