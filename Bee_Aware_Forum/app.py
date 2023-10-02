from flask import Flask, render_template, session, g, redirect, url_for
from datetime import datetime
from sqlalchemy import text
from flask_migrate import Migrate
from exts import db, mail
from models import UserModel
import config
from models import UserModel
from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
import time
import os


app = Flask(__name__)
# tide file
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)
if __name__ == '__main__':
    app.run()

