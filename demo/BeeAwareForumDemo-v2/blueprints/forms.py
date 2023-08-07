import wtforms
from wtforms.validators import Length, EqualTo, Email,InputRequired
from models import UserModel, QuestionModel

class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=3, max=50, message="wrong username type")])
    email = wtforms.StringField(validators=[Email(message="wrong email type")])
    password = wtforms.StringField(validators=[Length(min=6, max=50, message="wrong password type")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="must equal to password")])

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="The email has been registered")

class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=3, max=50, message="wrong username type")])
    password = wtforms.StringField(validators=[Length(min=6, max=50, message="wrong password type")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="wrong type in title")])
    content = wtforms.StringField(validators=[Length(min=3, message="wrong type in content")])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1, message="wrong type in content")])
    question_id=wtforms.IntegerField(validators=[InputRequired(message="must input Id")])