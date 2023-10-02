from flask import Blueprint, render_template, request, redirect, url_for, g,session
from .forms import QuestionForm, AnswerForm
from datetime import datetime, timedelta
from models import UserModel, QuestionModel, AnswerModel, History, SaveModel
from exts import db
from flask_sqlalchemy import SQLAlchemy

bp = Blueprint("qa", __name__, url_prefix="/")

@bp.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

@bp.context_processor
def my_context_processor():
    return {"user": g.user}


@bp.route("/", methods=['POST', 'GET'])
def index():
    per_page = 8
    now = datetime.now()
    days_ago = now - timedelta(days=5)
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        questions = QuestionModel.query.order_by(QuestionModel.create_Time.desc()).paginate(page=page, per_page=per_page)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(QuestionModel.NumOfLikes.desc()).all()
        if not g.user:
            histories = " "
            saves = " "
        else:
            histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
            saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
        return render_template("home_page.html", questions=questions, hot_posts=hot_posts, now=now, days_ago=days_ago, histories=histories, saves=saves, author=g.user)
    else:
        functionality = request.form['functionality']
        page = request.args.get('page', 1, type=int)
        questions = QuestionModel.query.order_by(QuestionModel.create_Time.desc()).paginate(page=page,per_page=per_page)
        if functionality == 'likes':
            hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(QuestionModel.NumOfLikes.desc()).all()
            if not g.user:
                histories = " "
                saves = " "
            else:
                histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
                saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
            return render_template("home_page.html", questions=questions, hot_posts=hot_posts, now=now, days_ago=days_ago,histories=histories, saves=saves, author=g.user)
        elif functionality == 'view':
            hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(QuestionModel.NumOfView.desc()).all()
            if not g.user:
                histories = " "
                saves = " "
            else:
                histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
                saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
            return render_template("home_page.html", questions=questions, hot_posts=hot_posts, now=now, days_ago=days_ago,histories=histories, saves=saves, author=g.user)


@bp.route("/qa/my_post", methods=['GET', 'POST'])
def public_my_post():
    if not g.user:
        return "Please login first"
    else:
        per_page = 8
        page = request.args.get('page', 1, type=int)
        # 获取当前用户发布的问题列表
        questions = QuestionModel.query.filter_by(author_id=g.user.id).order_by(QuestionModel.create_Time.desc()).paginate(page=page, per_page=per_page)
        return render_template("my_post.html", questions=questions, user=g.user)


@bp.route("/qa/like/<qa_id>", methods=['GET', 'POST'])
def qa_like(qa_id):
    question = QuestionModel.query.get(qa_id)
    if question:
        question.NumOfLikes += 1
        db.session.commit()
    return redirect(url_for("qa.index"))


@bp.route("/qa/dislike/<qa_id>", methods=['GET', 'POST'])
def qa_dislike(qa_id):
    question = QuestionModel.query.get(qa_id)
    if question:
        question.NumOfLikes -= 1
        db.session.commit()
    return redirect(url_for("qa.index"))


@bp.route("/qa/clicksave/<qa_id>")
def qa_clicksave(qa_id):
    if not g.user:
        return "Please login first"
    else:
        question = QuestionModel.query.get(qa_id)
        save_record = SaveModel.query.filter_by(user_id=g.user.id, question_id=question.id).first()
        if not save_record:
            save_record = SaveModel(user_id=g.user.id, question_id=question.id)
            db.session.add(save_record)
            db.session.commit()
        return redirect(url_for("qa.index", question=question))


@bp.route('/qa/my_post/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    question = QuestionModel.query.get(question_id)
    if question:
        db.session.delete(question)
        db.session.commit()
    return redirect(url_for('qa.public_my_post'))


@bp.route("/qa/post", methods=['GET', 'POST'])
def public_qa():
    if not g.user:
        return "Please login first"
    else:
        if request.method == 'GET':
            return render_template("post.html")
        else:
            form = QuestionForm(request.form)
            if form.validate():
                title = form.title.data
                content = form.content.data
                NumOfLikes = 0
                NumOfView = 0
                question = QuestionModel(title=title, content=content, NumOfLikes=NumOfLikes, NumOfView=NumOfView,
                                         author=g.user)
                db.session.add(question)
                db.session.commit()
                return redirect(url_for("qa.index"))
            else:
                print(form.errors)
                return redirect(url_for("qa.post"))

@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    if not g.user:
        return "Please login first"
    else:
        question = QuestionModel.query.get(qa_id)
        question.NumOfView += 1
        history_record = History.query.filter_by(user_id=g.user.id, question_id=question.id).first()
        if not history_record:
            history_record = History(user_id=g.user.id, question_id=question.id, created_time=datetime.now())
            db.session.add(history_record)
        else:
            history_record.created_time = datetime.now()
        db.session.commit()
        return render_template("detail.html", question=question)

# @bp.rout("/answer/public", method=['POST'])
@bp.post("/answer/public/")
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        NumOfLikes = 0
        answer_to_id = request.form.get('answer_to_id')
        answer_to_id = int(answer_to_id) if answer_to_id else None
        question_id = form.question_id.data
        last_answer = AnswerModel.query.filter_by(question_id=question_id, author_id=g.user.id).order_by(AnswerModel.create_Time.desc()).first()
        last_to_user = last_answer.author.username if last_answer else None
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id, answer_to_id=answer_to_id, last_to_user=last_to_user, NumOfLikes=NumOfLikes)
        if last_answer:
            answer.reply_info = f" to '{last_answer.content}' "
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))

@bp.route("/answer/like/<qa_id>", methods=['GET'])
def answer_like(qa_id):
    answer = AnswerModel.query.get(qa_id)
    if answer:
        answer.NumOfLikes += 1
        db.session.commit()
    return redirect(url_for("qa.qa_detail", qa_id=answer.question_id))


@bp.route("/answer/dislike/<qa_id>", methods=['GET'])
def answer_dislike(qa_id):
    answer = AnswerModel.query.get(qa_id)
    if answer:
        answer.NumOfLikes -= 1
        db.session.commit()
    return redirect(url_for("qa.qa_detail", qa_id=answer.question_id))


@bp.route('/history')
def history():
    if not g.user:
        return "Please login first"
    else:
        per_page = 8
        page = request.args.get('page', 1, type=int)
        histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).paginate(page=page, per_page=per_page)
        return render_template("history.html", histories=histories)


@bp.route('/save')
def save():
    if not g.user:
        return "Please login first"
    else:
        per_page = 8
        page = request.args.get('page', 1, type=int)
        saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).paginate(page=page, per_page=per_page)
        return render_template("save.html", saves=saves)


@bp.route('/save/delete/<int:question_id>', methods=['GET', 'POST'])
def delete_save(question_id):
    save = SaveModel.query.get((g.user.id, question_id))
    if save:
        db.session.delete(save)
        db.session.commit()
    return redirect(url_for('qa.save'))


@bp.route('/qa/profile', methods=['GET', 'POST'])
def profile():
    user = g.user
    if not user:
        return "Please login first"
    if request.method == 'POST':
        if 'update_username' in request.form:
            username = request.form['username']
            user.username = username
        if 'update_email' in request.form:
            email = request.form['email']
            user.email = email
        if 'update_address' in request.form:
            address = request.form['address']
            user.address = address
        if 'update_birthday' in request.form:
            birthday = request.form['birthday']
            user.birthday = birthday
        if 'update_introduction' in request.form:
            introduction = request.form['introduction']
            user.introduction = introduction
        db.session.commit()
        return redirect(url_for('qa.profile'))

    return render_template('profile.html', user=user)


@bp.route("/search")
def searchinhome():
    q= request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    now = datetime.now()
    days_ago = now - timedelta(days=5)
    hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(
        QuestionModel.NumOfLikes.desc()).all()
    return render_template("home_page.html", questions=questions, hot_posts=hot_posts)

