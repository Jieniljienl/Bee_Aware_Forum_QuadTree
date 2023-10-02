from flask import Blueprint, render_template, request, redirect, url_for, g,session,current_app,flash
from .forms import QuestionForm, AnswerForm
from datetime import datetime, timedelta
from models import UserModel, QuestionModel, AnswerModel, History, SaveModel
from exts import db
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os

bp = Blueprint("qa", __name__, url_prefix="/")
bp.config = {'UPLOAD_FOLDER': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'src')}
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def save_image(image):
    if image:
        image_filename = secure_filename(image.filename)
        image.save(os.path.join(bp.config['UPLOAD_FOLDER'], image_filename))
        return image_filename
    return None


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
    page = request.args.get('page', 1, type=int)
    questions = QuestionModel.query.order_by(QuestionModel.create_Time.desc()).paginate(page=page, per_page=per_page)
    hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(
        QuestionModel.NumOfLikes.desc()).all()
    if not g.user:
        histories = " "
        saves = " "
        my_posts= " "
    else:

        histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
        saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
        my_posts=QuestionModel.query.filter_by(author_id=g.user.id).order_by(QuestionModel.create_Time.desc()).all()
    return render_template("home_page.html", questions=questions, hot_posts=hot_posts, my_posts=my_posts,now=now, days_ago=days_ago,histories=histories, saves=saves, author=g.user)


@bp.route("/qa/my_post", methods=['GET', 'POST'])
def public_my_post():
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        per_page = 8
        page = request.args.get('page', 1, type=int)
        questions = QuestionModel.query.filter_by(author_id=g.user.id).order_by(QuestionModel.create_Time.desc()).paginate(page=page, per_page=per_page)
        now = datetime.now()
        days_ago = now - timedelta(days=5)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(
            QuestionModel.NumOfLikes.desc()).all()
        histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
        saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
        my_posts = QuestionModel.query.filter_by(author_id=g.user.id).order_by(
                QuestionModel.create_Time.desc()).all()
        return render_template("my_post.html", questions=questions, my_posts=my_posts,user=g.user,hot_posts=hot_posts, now=now, days_ago=days_ago,histories=histories, saves=saves, author=g.user)


@bp.route("/qa/like/<qa_id>", methods=['GET', 'POST'])
def qa_like(qa_id):
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        question = QuestionModel.query.get(qa_id)
        if question:
            question.NumOfLikes += 1
            if question.author.exp + 5 >= 150:
                question.author.exp = question.author.exp + 5 - 150
                question.author.level = question.author.level + 1
            else:
                question.author.exp = question.author.exp + 5
            db.session.commit()
        return redirect(url_for("qa.index"))


@bp.route("/qa/dislike/<qa_id>", methods=['GET', 'POST'])
def qa_dislike(qa_id):
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        question = QuestionModel.query.get(qa_id)
        if question:
            question.NumOfLikes -= 1
            db.session.commit()
        return redirect(url_for("qa.index"))


@bp.route("/qa/clicksave/<qa_id>")
def qa_clicksave(qa_id):
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        question = QuestionModel.query.get(qa_id)
        save_record = SaveModel.query.filter_by(user_id=g.user.id, question_id=question.id).first()
        if not save_record:
            save_record = SaveModel(user_id=g.user.id, question_id=question.id)
            db.session.add(save_record)
            db.session.commit()
        return redirect(url_for("qa.index", question=question))


@bp.route('/qa/my_post/delete/<int:question_id>', methods=['GET', 'POST'])
def delete_question(question_id):
    question = QuestionModel.query.get(question_id)
    if question:
        db.session.delete(question)
        db.session.commit()
    return redirect(url_for('qa.public_my_post'))



@bp.route("/qa/post", methods=['GET', 'POST'])
def public_qa():
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        post_records = QuestionModel.query.filter_by(author_id=g.user.id).count()+1
        now = datetime.now()
        days_ago = now - timedelta(days=5)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(
            QuestionModel.NumOfLikes.desc()).all()
        histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
        saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
        my_posts = QuestionModel.query.filter_by(author_id=g.user.id).order_by(
            QuestionModel.create_Time.desc()).all()
        if request.method == 'GET':
            return render_template("post.html",post_records=post_records,hot_posts=hot_posts, now=now,days_ago=days_ago, histories=histories, my_posts=my_posts,saves=saves, author=g.user)
        else:
            form = QuestionForm(request.form)
            if form.validate():
                title = form.title.data
                content = form.content.data
                NumOfLikes = 0
                NumOfView = 0
                tag = request.form['tag']
                image = request.files.get('image')
                image_filename = save_image(image)
                if image_filename:
                    question = QuestionModel(
                        title=title, content=content, NumOfLikes=NumOfLikes, NumOfView=NumOfView,
                        author=g.user, tag=tag, image_filename=image_filename
                    )
                else:
                    question = QuestionModel(
                        title=title, content=content, NumOfLikes=NumOfLikes, NumOfView=NumOfView,
                        author=g.user, tag=tag
                    )
                db.session.add(question)
                db.session.commit()
                if g.user.exp+30>=150:
                    g.user.exp=g.user.exp+30-150
                    g.user.level=g.user.level+1
                else:
                    g.user.exp=g.user.exp+30
                db.session.commit()
                return redirect(url_for("qa.index"))
            else:
                print(form.errors)
                return redirect(url_for("qa.index"))

@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        now = datetime.now()
        days_ago = now - timedelta(days=5)
        page = request.args.get('page', 1, type=int)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(
            QuestionModel.NumOfLikes.desc()).all()
        if not g.user:
            histories = " "
            saves = " "
        else:
            histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
            saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
        question = QuestionModel.query.get(qa_id)
        question.NumOfView += 1
        history_record = History.query.filter_by(user_id=g.user.id, question_id=question.id).first()
        if not history_record:
            history_record = History(user_id=g.user.id, question_id=question.id, created_time=datetime.now())
            db.session.add(history_record)
        else:
            history_record.created_time = datetime.now()
        db.session.commit()
        return render_template("detail.html", question=question,hot_posts=hot_posts, now=now,
                               days_ago=days_ago, histories=histories, saves=saves, author=g.user)

# @bp.rout("/answer/public", method=['POST'])
@bp.post("/answer/public/")
def public_answer():
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        form = AnswerForm(request.form)
        if form.validate():
            content = form.content.data
            question_id = form.question_id.data
            answer_to_id = int(request.form.get('answer_to_id')) if request.form.get('answer_to_id') else None

        # Get the last answer if it exists
            last_answer = AnswerModel.query.filter_by(id=answer_to_id).first()

        # Determine reply_info and last_to_user values
            reply_info = None
            last_to_user = None
            if last_answer:
                reply_info = f"to '{last_answer.content}'"
                last_to_user = last_answer.author.username
        # Create a new answer
            answer = AnswerModel(
                content=content,
                question_id=question_id,
                author_id=g.user.id,
                answer_to_id=answer_to_id,
                NumOfLikes=0,
                reply_info=reply_info,
                last_to_user=last_to_user
            )

            db.session.add(answer)
            db.session.commit()
            if g.user.exp + 10 >= 150:
                g.user.exp = g.user.exp + 10 - 150
                g.user.level = g.user.level + 1
            else:
                g.user.exp = g.user.exp + 10
            db.session.commit()
            return redirect(url_for("qa.qa_detail", qa_id=question_id))
        else:
            print(form.errors)
            return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))

@bp.route("/answer/like/<qa_id>", methods=['GET'])
def answer_like(qa_id):
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        answer = AnswerModel.query.get(qa_id)
        if answer:
            answer.NumOfLikes += 1
            if answer.author.exp + 2 >= 150:
                answer.author.exp = answer.author.exp + 2 - 150
                answer.author.level = answer.author.level + 2
            else:
                answer.author.exp = answer.author.exp + 2
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=answer.question_id))


@bp.route("/answer/dislike/<qa_id>", methods=['GET'])
def answer_dislike(qa_id):
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        answer = AnswerModel.query.get(qa_id)
        if answer:
            answer.NumOfLikes -= 1
            db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=answer.question_id))

@bp.route("/qa/detail/like/<qa_id>", methods=['GET', 'POST'])
def qa_like_in_detail(qa_id):
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        question = QuestionModel.query.get(qa_id)
        if question:
            question.NumOfLikes += 1
            if question.author.exp + 5 >= 150:
                question.author.exp = question.author.exp + 5 - 150
                question.author.level = question.author.level + 1
            else:
                question.author.exp = question.author.exp + 5
            db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question.id))

@bp.route("/qa/detail/dislike/<qa_id>", methods=['GET', 'POST'])
def qa_dislike_in_detail(qa_id):
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        question = QuestionModel.query.get(qa_id)
        if question:
            question.NumOfLikes -= 1
            db.session.commit()
        return redirect(url_for("qa.qa_detail",qa_id=question.id))

@bp.route('/history')
def history():
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        per_page = 8
        page = request.args.get('page', 1, type=int)
        histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).paginate(page=page, per_page=per_page)
        now = datetime.now()
        days_ago = now - timedelta(days=5)
        page = request.args.get('page', 1, type=int)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(
            QuestionModel.NumOfLikes.desc()).all()
        if not g.user:
            histories1 = " "
            saves = " "
        else:
            histories1 = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
            saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
        return render_template("history.html", histories=histories,hot_posts=hot_posts, now=now, days_ago=days_ago,histories1=histories1, saves=saves, author=g.user)


@bp.route('/save')
def save():
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        per_page = 8
        page = request.args.get('page', 1, type=int)
        saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).paginate(page=page, per_page=per_page)
        now = datetime.now()
        days_ago = now - timedelta(days=5)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(
            QuestionModel.NumOfLikes.desc()).all()
        if not g.user:
            histories = " "
            saves1 = " "
        else:
            histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
            saves1 = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
        return render_template("save.html", saves=saves, hot_posts=hot_posts, now=now,days_ago=days_ago, histories=histories, saves1=saves1, author=g.user)


@bp.route('/save/delete/<int:question_id>', methods=['GET', 'POST'])
def delete_save(question_id):
    save = SaveModel.query.get((g.user.id, question_id))
    if save:
        db.session.delete(save)
        db.session.commit()
    return redirect(url_for('qa.save'))



@bp.route('/history/delete/<int:question_id>', methods=['GET', 'POST'])
def delete_history(question_id):
    history = History.query.get((g.user.id, question_id))
    if history:
        db.session.delete(history)
        db.session.commit()
    return redirect(url_for('qa.history'))


@bp.route('/qa/profile', methods=['GET', 'POST'])
def profile():
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        user = g.user
        now = datetime.now()
        Questions=QuestionModel.query.filter_by(author_id=g.user.id)
        Answers=AnswerModel.query.filter_by(author_id=g.user.id)
        days_ago = now - timedelta(days=5)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(
            QuestionModel.NumOfLikes.desc()).all()
        post_records = QuestionModel.query.filter_by(author_id=g.user.id).count()
        favourite_records= SaveModel.query.filter_by(user_id=g.user.id).count()
        history_records = History.query.filter_by(user_id=g.user.id).count()
        likes_records= 0
        for question1 in Questions:
            likes_records=question1.NumOfLikes+likes_records
        for answer1 in Answers:
            likes_records=answer1.NumOfLikes+likes_records
        if not g.user:
            histories = " "
            saves = " "
        else:
            histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
            saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
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
            image = request.files.get('image')
            image_filename = save_image(image)
            if image_filename:
                user.image_filename=image_filename
            db.session.commit()
            return redirect(url_for('qa.profile'))
        return render_template('profile.html', user=user, hot_posts=hot_posts, history_records=history_records,likes_records=likes_records,favourite_records=favourite_records, post_records=post_records,now=now, days_ago=days_ago,histories=histories, saves=saves, author=g.user)


@bp.route('/qa/other_profile/<int:user_id>', methods=['GET', 'POST'])
def other_profile(user_id):
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        user = UserModel.query.get(user_id)
        now = datetime.now()
        Questions=QuestionModel.query.filter_by(author_id=g.user.id)
        Answers=AnswerModel.query.filter_by(author_id=g.user.id)
        days_ago = now - timedelta(days=5)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(
            QuestionModel.NumOfLikes.desc()).all()
        post_records = QuestionModel.query.filter_by(author_id=g.user.id).count()
        favourite_records= SaveModel.query.filter_by(user_id=g.user.id).count()
        history_records = History.query.filter_by(user_id=g.user.id).count()
        likes_records= 0
        for question1 in Questions:
            likes_records=question1.NumOfLikes+likes_records
        for answer1 in Answers:
            likes_records=answer1.NumOfLikes+likes_records
        if not g.user:
            histories = " "
            saves = " "
        else:
            histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
            saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
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
            image = request.files.get('image')
            image_filename = save_image(image)
            if image_filename:
                user.image_filename=image_filename
        return render_template('other_profile.html', user=user, hot_posts=hot_posts, history_records=history_records,likes_records=likes_records,favourite_records=favourite_records, post_records=post_records,now=now, days_ago=days_ago,histories=histories, saves=saves, author=g.user)


@bp.route("/index/search")
def searchinhome():
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        q= request.args.get("q")
        per_page = 8
        page = request.args.get('page', 1, type=int)
        questions = QuestionModel.query.filter(
            or_(QuestionModel.title.contains(q), QuestionModel.content.contains(q))
        ).paginate(page=page, per_page=per_page)
        now = datetime.now()
        days_ago = now - timedelta(days=5)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(QuestionModel.NumOfLikes.desc()).all()
        histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
        my_posts = QuestionModel.query.filter_by(author_id=g.user.id).order_by(
            QuestionModel.create_Time.desc()).all()
        saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
        return render_template("home_page.html", questions=questions, my_posts=my_posts,hot_posts=hot_posts,histories=histories,saves=saves)

@bp.route("/index/searchtag")
def searchintag():
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        tag = request.args.get("t")
        per_page = 8
        page = request.args.get('page', 1, type=int)
        questions = QuestionModel.query.filter_by(tag=tag).paginate(page=page, per_page=per_page)
        now = datetime.now()
        days_ago = now - timedelta(days=5)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(
            QuestionModel.NumOfLikes.desc()).all()
        my_posts = QuestionModel.query.filter_by(author_id=g.user.id).order_by(
            QuestionModel.create_Time.desc()).all()
        histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
        saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
        return render_template("home_page.html", questions=questions, my_posts=my_posts, hot_posts=hot_posts, histories=histories, saves=saves)


@bp.route('/index/filter_by_date', methods=['GET'])
def filter_by_date():
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        current_date = datetime.date
        date = request.args.get("date")
        selected_date_str = request.args.get("date")
        per_page = 8
        if not selected_date_str:
            selected_date = datetime.now().date()
        else:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d')
            selected_date = selected_date.replace(hour=23, minute=59, second=59, microsecond=59)
        page = request.args.get('page', 1, type=int)
        questions = QuestionModel.query.filter(QuestionModel.create_Time <= selected_date).order_by(
            QuestionModel.create_Time.desc()).paginate(page=page, per_page=per_page)
        now = datetime.now()
        days_ago = now - timedelta(days=5)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(
            QuestionModel.NumOfLikes.desc()).all()
        my_posts = QuestionModel.query.filter_by(author_id=g.user.id).order_by(
            QuestionModel.create_Time.desc()).all()
        histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
        saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
        return render_template("home_page.html", questions=questions, current_date=current_date, selected_date=selected_date, my_posts=my_posts,hot_posts=hot_posts, histories=histories, saves=saves)

@bp.route("/my_post/search")
def searchinpost():
    if not g.user:
        return redirect(url_for("auth.login"))
    else:
        q= request.args.get("q")
        per_page = 8
        page = request.args.get('page', 1, type=int)
        questions1 = QuestionModel.query.filter_by(author_id=g.user.id).order_by(QuestionModel.create_Time.desc()).all()

        # 执行问题搜索，标题或内容包含搜索词 q
        questions = QuestionModel.query.filter(
            (QuestionModel.author_id == g.user.id) &
            (or_(QuestionModel.title.contains(q), QuestionModel.content.contains(q)))
        ).paginate(page=page, per_page=per_page)
        now = datetime.now()
        days_ago = now - timedelta(days=5)
        hot_posts = QuestionModel.query.filter(QuestionModel.create_Time > days_ago).order_by(QuestionModel.NumOfLikes.desc()).all()
        histories = History.query.filter_by(user_id=g.user.id).order_by(History.created_time.desc()).all()
        my_posts = QuestionModel.query.filter_by(author_id=g.user.id).order_by(
            QuestionModel.create_Time.desc()).all()
        saves = SaveModel.query.filter_by(user_id=g.user.id).order_by(SaveModel.created_time.desc()).all()
        return render_template("my_post.html", questions=questions, my_posts=my_posts,hot_posts=hot_posts,histories=histories,saves=saves)