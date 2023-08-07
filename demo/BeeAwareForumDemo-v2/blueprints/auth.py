
from flask import session, Blueprint, render_template, request, jsonify, redirect, url_for
from .forms import RegisterForm, LoginForm

from datetime import date
from models import UserModel
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = UserModel.query.filter_by(username=username).first()
            if not  user:
                print("No user")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for("qa.index"))
            else:
                print("Wrong password")
                return redirect(url_for("auth.login"))

        else:
            print(form.errors)
            return redirect(url_for("auth.login"))

@bp.route("/register",  methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            birthday = date(2000, 1, 1)
            address = "None"
            introduction = "None"
            user = UserModel(email=email, username=username, address=address, birthday=birthday, introduction=introduction, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))



