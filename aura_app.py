from app import create_app
from app.models import db

app = create_app('ProductionConfig')




# if __name__ == '__main__': # code was commented out to set enivornment for render
with app.app_context(): # code was indented out one tab.
        #db.drop_all()
        db.create_all()
    
    # app.run(debug=True) # code was commented out to set up enivornment for render