from flask import Flask
from flask_migrate import Migrate

from Project5.config import Config
from Project5.models import db
migrate = Migrate()


app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
migrate.init_app(app, db)

from Project5.views import *