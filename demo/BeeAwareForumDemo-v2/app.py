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

app = Flask(__name__)
# tide file
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)

@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

@app.context_processor
def my_context_processor():
    return {"user":g.user}

if __name__ == '__main__':
    app.run()
