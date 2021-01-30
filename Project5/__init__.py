from flask import Flask

from Project5.config import Config
from Project5.models import db


app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)


from Project5.views import *