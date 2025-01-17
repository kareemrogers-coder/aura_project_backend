from app import create_app
from app.models import db
import json
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# from app.utils import token_required, verfiy_token
#app = create_app('DevelopmentConfig')
app = create_app('ProductionConfig')
jwt= JWTManager(app) ###new
CORS(app)


Auth0_Domain = "dev-y870izsbr3wx4epg.us.auth0.com" #kareem
# Auth0_Domain = "dev-3niskqr7oyd1o1x3.us.auth0.com" #zab
API_IDENTIFIER = "this-is-our-logo-generator-app-project."
# API_IDENTIFIER = "aura-gen"
ALGOTITHMS = ["RS256"]


#if __name__ == '__main__': # code was commented out to set enivornment for render
with app.app_context(): # code was indented out one tab.
                #db.drop_all()
                db.create_all()
    
#app.run(debug=True) # code was commented out to set up enivornment for render