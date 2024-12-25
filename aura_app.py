from app import create_app
from app.models import db
# from app.utils import token_required, verfiy_token

app = create_app('ProductionConfig')

# app = create_app('DevelopmentConfig')

Auth0_Domain = "dev-y870izsbr3wx4epg.us.auth0.com"
API_IDENTIFIER = "this-is-our-logo-generator-app-project."
ALGOTITHMS = ["RS256"]


# if __name__ == '__main__': # code was commented out to set enivornment for render
with app.app_context(): # code was indented out one tab.
        #db.drop_all()
        db.create_all()
    
    # app.run(debug=True) # code was commented out to set up enivornment for render