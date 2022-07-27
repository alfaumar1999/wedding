#instantiate an object of flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from weddingapp import config





app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config.from_object(config.LiveConfig)

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
# migrate = Migrate(app,db)

#import anything that would be used site-wide or globally

from weddingapp import models
from weddingapp.routes import admin_routes,user_routes

#you can also import any other variable,object,module you would need in this aoo
