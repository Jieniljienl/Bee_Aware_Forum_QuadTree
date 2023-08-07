from datetime import date
import re
from flask import Flask
from flask import render_template
from flask import Markup
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask import flash, request
from werkzeug.utils import secure_filename
import os
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import redirect
from datetime import datetime
import uuid

app = Flask(__name__, static_folder='static')
app.secret_key = 'jk!d;dffa.fd#95asd[d*ds[]xc[a]z'
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'static/image/')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
db = SQLAlchemy(app)


# User Table （用户表）
class Users(db.Model):
    # id = db.Column(db.Integer(), primary_key=True)
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(70))
    email_id = db.Column(db.String(50))
    password = db.Column(db.String(30))
    contactNumber = db.Column(db.String(11))
    myPosts = db.relationship('Posts', backref='poster')

    favorites = db.relationship('Posts', secondary='user_favorite_post')
    history = db.relationship('Posts', secondary='user_history_post')

# Post Table (帖子表)
class Posts(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    poster_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    img_src = db.Column(db.Text)
    postDate = db.Column(db.Date)
    postTime = db.Column(db.Time)

# Association Table(User and saved posts) 中间表(用户和收藏帖子)
user_favorite_post = db.Table('user_favorite_post',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)
# Association Table(user and history posts) 中间表(用户和历史帖子)
user_history_post = db.Table('user_history_post',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)


# 路由管理
@app.route('/')
def bootroute():
    return redirect(url_for('index'))


# HomePage 未登录
@app.route('/index/', methods=['GET','POST'])
def index():
    # posts = Posts.query.filter().all()
    posts = Posts.query.order_by(Posts.postDate.desc(), Posts.postTime.desc()).all()
    return render_template('_index.html', anonymity=True,user=None, posts=posts)


# HomePage 已登录
@app.route('/index/<id>/', methods=['GET','POST'])
def index_username(id):
    user = Users.query.filter(Users.id == id).first()
    # posts = Posts.query.filter().all()
    posts = Posts.query.order_by(Posts.postDate.desc(), Posts.postTime.desc()).all()
    print(posts)
    return render_template('_index.html', anonymity=False, user=user, posts=posts)

# 用户登录路由
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # return render_template('_login.html')
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')

        # 判断信息完整
        if id == "":
            flash('Parameter Incomplete')
            print('login:Parameter Incomplete')
        elif password == "":
            flash('Parameter Incomplete')
            print('login:Parameter Incomplete')

        user = Users.query.filter(Users.id == id, Users.password == password).first()

        print('login' + str(user))
        if user:
            id = user.id
            return redirect(url_for('index_username', id=id))
            # return render_template('_login.html')
        else:
            # return "login fail"
            flash('登录失败，请重新登录')
            return render_template('_login.html')
    return render_template('_login.html')


# 用户注册路由
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # id = request.form.get('id')
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        contactNum = request.form.get('contact_num')

        # 输出表单信息
        print(id)
        print(name)
        print(email)
        print(password)
        print(password2)
        print(contactNum)

        if name == "":
            flash('Parameter Incomplete')
            print('Parameter Incomplete')

        elif email == "":
            flash('Parameter Incomplete')
            print('Parameter Incomplete')
        elif password == "":
            flash('Parameter Incomplete')
            print('Parameter Incomplete')
        elif password2 == "":
            flash('Parameter Incomplete')
            print('Parameter Incomplete')
        elif contactNum == "":
            flash('Parameter Incomplete')
            print('Parameter Incomplete')
            # 密码匹配
        elif password != password2:
            flash('The two passwords do not match. Please re-enter them')
            print('The two passwords do not match. Please re-enter them')
        else:
            print('OK1')
            new_user = Users(name=name, email_id=email, password=password, contactNumber=contactNum)
            db.session.add(new_user)
            
            db.session.commit()
            flash('注册成功，请登录')
            print('OK2')
            return redirect(url_for('login'))
    return render_template('_register.html')


# # 活动详情页面
# @app.route('/detail/<id>')
# def detail(id):
#     post = Posts.query.filter(Posts.id == int(id)).first()
#     print(post)
#     print("Now the userID is :")
#     print(id)
#     return render_template('_detail.html', id=id, post=post)

# 活动详情页面(未登录)
@app.route('/detail/<post_id>/')
def detail_anonymity(post_id):
    post = Posts.query.filter(Posts.id == int(post_id)).first()
    return render_template('_detail.html', anonymity=True, user=None, post=post)

# 活动详情页面(已经登陆)
@app.route('/detail/<user_id>/<post_id>/')
def detail(user_id, post_id):
    post = Posts.query.filter(Posts.id == int(post_id)).first()
    user = Users.query.filter(Users.id == user_id).first()
    print(post)
    print("Now the userID is :")
    print(user.id)
    return render_template('_detail.html', anonymity=False, user=user, post=post)

# favorites route(收藏夹路由)
@app.route('/favorites/<id>/', methods=['GET','POST'])
def favorites(id):
    user = Users.query.filter(Users.id == id).first()
    saved_posts = user.favorites
    return render_template('_favorites.html', user=user, posts=saved_posts)


# add_romove_favorite route (收藏或取消收藏路由)
@app.route('/add_romove_favorite/', methods=['GET','POST'])
def add_romove_favorite():
    if request.method == 'POST':
        print(request.form)
        post_id = int(request.form.get('post_id'))
        user_id = int(request.form.get('user_id'))
        print(post_id)
        print(user_id)
        print("----------")
        user = Users.query.filter(Users.id == user_id).first()
        post = Posts.query.filter(Posts.id == post_id).first()
        print(user)
        print(post)
        print("----------")
        print(user.favorites)
        print(request.referrer)
        
        if post in user.favorites:
            user.favorites.remove(post)
            db.session.commit()
            print('Post removed from favorites', 'success')
            
            return redirect(request.referrer)
        else:
            user.favorites.append(post)
            db.session.commit()
            print('Post added to favorites', 'success')
            return redirect(request.referrer)
        
    return render_template('_favorite.html', anonymity=False, id=id, posts=user.favorites)

# history posts route (历史帖子路由)
@app.route('/history/<id>/', methods=['GET','POST'])
def history(id):
    user = Users.query.filter(Users.id == id).first()
    history_posts = user.history
    return render_template('_history.html', user=user, posts=history_posts)
    
# add_romove_history route (添加到历史路由)
@app.route('/add_romove_history/', methods=['GET','POST'])
def add_romove_history():
    print("history route boot")
    if request.method == 'POST':
        print(request.form)
        append_or_remove = request.form.get('append_or_remove')
        post_id = int(request.form.get('post_id'))
        user_id = int(request.form.get('user_id'))
        print(append_or_remove)
        print(post_id)
        print(user_id)
        print("----------")
        user = Users.query.filter(Users.id == user_id).first()
        post = Posts.query.filter(Posts.id == post_id).first()
        print(user)
        print(post)
        print("----------")
        print(user.history)
        print(request.referrer)
        if append_or_remove == "remove":
            user.history.remove(post)
            db.session.commit()
            return redirect(request.referrer) # 在历史帖子页面时
        elif append_or_remove == "append":
            if post not in user.history:
                user.history.append(post)
                db.session.commit()
                return redirect(url_for('detail', user_id=user.id, post_id=post.id)) # 点击click to learn more时
            else: return redirect(url_for('detail', user_id=user.id, post_id=post.id))

    return render_template('_history.html', anonymity=False, id=id, posts=user.history)

# 文件上传路由
@app.route('/uploader/', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        # id = request.form.get('id')
        poster_id = request.form.get('poster_id')
        title = request.form.get('title')
        text = request.form.get('text')
        postDate = request.form.get('postDate')
        postTime = request.form.get('postTime')
        # print("这是接受到的表单数据：") # debuge
        # print(id)
        # print(title)
        # print(text)
        # print(postDate)
        # print(postTime)
        # 保存图片文件
        img = request.files['file']
        UPLOAD_PATH_converted = app.config['UPLOAD_PATH'].replace("\\", "/")
        # 重命名图片
        # img.filename = str(2) + '.jpg '
        img.filename = str(uuid.uuid4()) + '.jpg '

        
        upload_path = os.path.join(UPLOAD_PATH_converted, secure_filename(img.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        img.save(upload_path)
        img_src = ''
        # img_src= upload_path
        img_src = os.path.join('http://127.0.0.1:5000/static/image/', secure_filename(img.filename))

        date_ = datetime.strptime(postDate, "%Y-%m-%d").date()
        time_ = datetime.strptime(postTime, "%H:%M").time()
        # time_ = datetime.time(time)
        # time_ = time
        # print("信息存入数据库前一切完好")
        # 判断信息完整性
        if id == "":
            flash('Para.meter Incomplete')
            print('Parameter Incomplete')
        elif title == "":
            flash('Parameter Incomplete')
            print('Parameter Incomplete')
        elif postDate == "":
            flash('Parameter Incomplete')
            print('Parameter Incomplete')
        elif postTime == "":
            flash('Parameter Incomplete')
            print('Parameter Incomplete')
        elif text == "":
            flash('Parameter Incomplete')
            print('Parameter Incomplete')
        elif img_src == "":
            flash('Parameter Incomplete')
            print('Parameter Incomplete')
        else:
            print("Post OK 1")
            
            new_post = Posts(poster_id=poster_id, title=title, postDate=date_, postTime=time_, text=text,
                                 img_src=img_src)
            print("almost success")
            db.session.add(new_post)
            db.session.commit()

            # 添加关系到中间表
            user = Users.query.filter(Users.id == poster_id).first()
            # print("09999999999009090009::::")
            # print(poster_id)
            # user = Users.query.filter(Users.id == poster_id).first()
            # user.favorites.append(new_post)
            # db.session.commit()

            # print('Post OK 2')
            return render_template('success_return.html', id=user.id)

        # return 'file uploaded successfully'

    else:

        return render_template('_create.html')


# 创建帖子路由
@app.route('/create/<id>/', methods=['GET', 'POST'])
def create(id):
    user = Users.query.filter(Users.id == id).first()
    posterId = user.id
    print("123123123131232131323123131312312313::::")
    print(posterId)
    print(user.id)
    return render_template('_create.html', user=user)


# 测试路由
@app.route('/test/', methods=['GET', 'POST'])
def test():
    flash('这是测试路由')
    return '测试'


# 全局变量定义
@app.context_processor
def abcd_convey():
    a = 'aaa'
    b = 'bbb'
    c = 'ccc'
    d = 'ddd'
    return dict(a=a, b=b, c=c, d=d)


# 全局函数定义
@app.template_global()
def set_href_detail(id): 
    return 'http://127.0.0.1:5000/detail/' + str(id)

# 全局函数定义
@app.template_global()
def set_href_index(user_id): 
    return 'http://127.0.0.1:5000/index/' + str(user_id)

# 全局函数定义
@app.template_global()
def set_href_detail_anonymity(post_id): 
    return 'http://127.0.0.1:5000/detail/' + str(post_id)

# 全局函数定义
@app.template_global()
def set_href_detail(user_id,post_id): 
    return 'http://127.0.0.1:5000/detail/' + str(user_id) + '/' + str(post_id)

with app.app_context():
    db.create_all()
    if __name__ == '__main__':
        app.run()
