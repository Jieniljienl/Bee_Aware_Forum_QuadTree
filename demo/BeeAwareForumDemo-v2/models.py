from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    birthday = db.Column(db.Date)
    introduction = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)


class History(db.Model):
    __tablename__ = 'user_question_history'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    created_time = db.Column(db.DateTime, default=datetime.now)
    question = db.relationship('QuestionModel', backref=db.backref('user_history', cascade='all, delete-orphan'))
    user = db.relationship('UserModel', backref=db.backref('question_history', cascade='all, delete-orphan'))


class SaveModel(db.Model):
    __tablename__ = 'user_question_save'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    created_time = db.Column(db.DateTime, default=datetime.now)
    question = db.relationship('QuestionModel', backref=db.backref('user_save', cascade='all, delete-orphan'))
    user = db.relationship('UserModel', backref=db.backref('question_save', cascade='all, delete-orphan'))
class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_Time = db.Column(db.DateTime, default=datetime.now)
    NumOfLikes = db.Column(db.Integer, nullable=False)
    NumOfView = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="questions")

class AnswerModel(db.Model):
    __tablename__="answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_Time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    question = db.relationship(QuestionModel,backref=db.backref("answers", order_by=create_Time.desc()))
    author = db.relationship(UserModel,backref=db.backref("answers", order_by=create_Time.desc()))