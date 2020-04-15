from flask import Flask
from config import config
from ac_database import AnonCommentDatabase

app = Flask(__name__)
app.config.from_object(config['default'])
acdb = AnonCommentDatabase(app)
acdb.init_database()

from app import routes
