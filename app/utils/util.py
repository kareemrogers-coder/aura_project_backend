# import jwt
import os
from datetime import datetime, timedelta, timezone
from  functools import wraps
from flask import request, jsonify,Flask
# from flask_cors import CORS
from urllib.request import urlopen
import json
from jose import jwt,jwe
import requests
from flask_jwt_extended import decode_token, create_access_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

Auth0_Domain = "dev-y870izsbr3wx4epg.us.auth0.com"
# Auth0_Domain = "dev-3niskqr7oyd1o1x3.us.auth0.com"
API_IDENTIFIER = "this-is-our-logo-generator-app-project."
ALGORITHMS = ["RS256"]
#ALGORITHMS = ["HS256"]

import config


SECRET_KEY = os.environ.get('SECRET_KEY') #THIS IS BEING PULL FROM .ENV.


def token_generator(email):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'email': email,
        'exp': expiration_time
    }
    private_key = open("private.key","r").read()
    return jwt.encode(payload, private_key, algorithm='RS256') # change back to RS256
    # secret_key = config('SECRET_KEY')
    # return jwt.encode(payload, secret_key, algorithms = 'RS256')




#TOKEN CREATION 
def encode_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days= 0, hours = 2),
        'iat': datetime.now(timezone.utc), 
        'sub': user_id
    }

    token = jwt.encode(payload, SECRET_KEY, algorithms ='RS256') #HS256 RS256



def verify_token(token):
    print("Verifying token")

    print("Opening URL")
    jsonurl = urlopen(f"https://{Auth0_Domain}/.well-known/jwks.json")

    # print("Reading json")
    jwks = json.loads(jsonurl.read())

    # print("Checking verified header")
    unverified_header = jwt.get_unverified_header(token)
    print("Unverified header:", unverified_header) # debug

    # if "alg" in unverified_header:
    #     print(f"Algorithm used in JWT: {unverified_header['alg']}")
    # else:
    #     print("No Algorithm found in JWT header")

    # if unverified_header and unverified_header["alg"] == "dir":
    #     print("Using symmetric key for verification (dir algorithms)")
    #     secret_key = SECRET_KEY
    #     try:
    #         payload = jwt.decode(
    #                 token,
    #                 options={"verify_signature": False},
    #                 algorithms=['dir'],
    #                 key=None,
    #                 audience= API_IDENTIFIER,
    #                 issuer=f"https://{Auth0_Domain}/",)#token, sercet_key, algorithms= ['dir']
    #         print('Payload:', payload)
    #         return payload
    #     except Exception as e:
    #         raise ValueError(f"Unable to verify token: {e}")


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
                    issuer=f"https://{Auth0_Domain}/",
                )
                print('PAYLOAD:', payload)
                return payload
            
        

        
            except jwt.ExpiredSignatureError:
                raise ValueError ("Token is expired.")
            except jwt.JWTClaimsError:
                raise ValueError("Incorrect claims. Check the audience and issuer.")
            except Exception as e:
                raise ValueError(f"unable to verify autheication token: {e}")
        else:
            raise ValueError("No matching RSA Key")
    




def token_required(f):
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", None)
        if not auth:
            return jsonify({"message": "Authorization header is missing"}), 401
        
        if "Bearer" not in auth:
            return jsonify({"message": "Bearer <Token> required"}), 401

        try:
            #Authorization: "Bearer <token>"
            token = auth.split()[1]
            payload = verify_token(token) #Sending token to be decrypted
        except ValueError as e:
            return jsonify({"message": str(e)}), 401

        return f(payload, *args, **kwargs)

    return decorated