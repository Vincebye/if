# -*- coding:utf8 -*-

from application import app, db
from flask import render_template, redirect, request, flash, get_flashed_messages, url_for, send_from_directory
from application.models import Image, User, Comment
from flask_login import current_user, login_user, logout_user, login_required
import hashlib, random, json, uuid, os
from email import send_email
from qiniusdk import save_file_to_cloud


from application.reglogin.forms import LoginForm, RegisterForm

# 首页
@app.route('/')
def index():
    images = Image.query.order_by('id desc').paginate(1, 5, False)
    return render_template('index.html', images = images.items)

# 首页ajax 的json 数据
@app.route('/images/<int:page_num>/<int:per_page>/')
def index_paginate(page_num, per_page):
    images = Image.query.order_by('id desc').paginate(page=page_num, per_page=per_page, error_out=False)
    map = {'has_next' : images.has_next}
    image = []
    for item in images.items:
        comment_user_username = []
        comment_user_id = []
        comment_content = []
        for comments_i in item.comments:
            comment_user_username.append(comments_i.user.username)
            comment_user_id.append(comments_i.user.id)
            comment_content.append(comments_i.content)

        imgov = {'image_user_id': item.user.id, 'image_user_head_url': item.user.head_url, 'image_user_username': item.user.username,
                 'image_id':item.id, 'image_url':item.url, 'image_comments_length':len(item.comments), 'comment_user_username': comment_user_username,
                 'comment_user_id':comment_user_id, 'comment_content':comment_content}

        image.append(imgov)

    map['images'] = image
    return json.dumps(map)

# 图片详情页
@app.route('/image/<int:id>/')
def image(id):
    images = Image.query.get(id)
    if images == None:
        return redirect('/')
    return render_template('pageDetail.html', images = images)

# 个人详情页
@app.route('/profile/<int:id>/')
@login_required
def profile(id):
    user = User.query.get(id)
    if user == None:
        return redirect('/')
    images = user.images.paginate(1, 6, False)
    return render_template('profile.html', user = user, images = images.items, has_next = images.has_next)

# 个人详情页 ajax 数据
@app.route('/profile/images/<int:id>/<int:page_num>/<int:per_page>/')
@login_required
def profile_paginate(id, page_num, per_page):
    user = User.query.get(id)
    paginate = user.images.paginate(page=page_num, per_page=per_page, error_out=False)
    map = {'has_next' : paginate.has_next}
    images = []
    for image in paginate.items:
        imgvo = {'id':image.id, 'url':image.url}
        images.append(imgvo)
    map['images'] = images
    return json.dumps(map)

# 旧版登陆注册界面
@app.route('/regloginpage/')
def regloginpage(msg = ''):
    if current_user.is_authenticated:
        return redirect('/')

    next = request.values.get('next')
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    return render_template('login.html', msg = msg, next = next)

# 旧版注册
@app.route('/reg/', methods=['POST', 'GET'])
def reg():
    username = unicode(request.values.get('username')).strip()
    password = unicode(request.values.get('password')).strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage/', u'用户名或密码不能为空', 'reglogin')

    user = User.query.filter_by(username = username).first()
    if user != None:
        return redirect_with_msg('/regloginpage/', u'用户名已经存在，请直接登陆', 'reglogin')

    salt = '.'.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 10))
    m = hashlib.md5()
    m.update(password + salt)
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    next_url = request.values.get('next')
    if next_url != None and next_url.startswith('/'):
        return redirect(next_url)

    return redirect('/profile/' + str(user.id))


def redirect_with_msg(url, msg, categroy=''):
    if msg != None:
        flash(msg, category=categroy)
    return redirect(url)

# 旧版登陆
@app.route('/login/', methods=['GET', 'POST'])
def login():
    username = unicode(request.values.get('username')).strip()
    password = unicode(request.values.get('password')).strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage/', u'用户名或密码不能为空', 'reglogin')

    user = User.query.filter_by(username = username).first()
    if user == None:
        return redirect_with_msg('/regloginpage/', u'用户名不存在', 'reglogin')

    m = hashlib.md5()
    m.update(password + user.salt)
    password = m.hexdigest()

    if password != user.password:
        return redirect_with_msg('/regloginpage/', u'密码不正确', 'reglogin')

    print user, user.is_active
    ret = login_user(user)
    print 'ret', ret

    next_url = request.values.get('next')
    if next_url != None and next_url.startswith('/'):
        return redirect(next_url)

    return redirect('/profile/' + str(user.id))

# 登出
@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/wtf/login/')

# 新版登陆
@app.route('/wtf/login/', methods=['GET', 'POST'])
def wtf_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None:
            m = hashlib.md5()
            m.update(form.password.data + user.salt)
            password = m.hexdigest()

            if password != user.password:
                return redirect_with_msg('/wtf/login/', u'密码不正确', 'login')

            login_user(user)

            next = request.args.get('next')
            if next != None:
                return redirect(request.args.get('next'))
            return redirect('/profile/' + unicode(user.id))
            flash('用户不存在.')
    return render_template('reglogin/reglogin_login.html', form = form)

# 新版注册
@app.route('/wtf/register/', methods=['GET', 'POST'])
def wtf_register():
    form = RegisterForm()
    if form.validate_on_submit():
        # add noise
        salt = '.'.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 10))
        password = form.password.data
        m = hashlib.md5()
        m.update(password + salt)
        password = m.hexdigest()
        user = User(form.username.data, form.email.data, password, salt)
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        send_email(form.email.data, u'Please activate your account', u'mail/new_user', user=user, token = token)

        login_user(user)
        next = request.args.get('next')
        if next != None:
            return redirect(request.args.get('next'))
        return redirect('/profile/' + unicode(user.id))
    return render_template('reglogin/reglogin_register.html', form = form)

def save_to_local(file, file_name):
    save_dir = os.path.join(os.getcwd(), app.config['UPLOAD_DIR'])
    file.save(os.path.join(save_dir, file_name))
    return '/image/' + file_name

@app.route('/image/<image_name>')
def view_image(image_name):
    save_dir = os.path.join(os.getcwd(), app.config['UPLOAD_DIR'])
    return send_from_directory(save_dir, image_name)

@app.route('/upload/', methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
        if file_ext in app.config['ALLOWED_EXT']:
            file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
            if app.config['SAVE_IN_LOCAL'] == True:
                url = save_to_local(file, file_name)
            else:
                url = save_file_to_cloud(file_name, file)
            if url != None:
                db.session.add(Image(url, current_user.id))
                db.session.commit()

    return redirect_with_msg('/profile/%d/' % current_user.id, '图片上传成功')


@app.route('/addcomment/', methods=['POST'])
@login_required
def addcomment():
    image_id = int(request.values['image_id'])
    content = request.values['content'].strip()
    comment = Comment(content, image_id, current_user.id)
    db.session.add(comment)
    db.session.commit()
    map = {'user_id':current_user.id, 'username' : current_user.username, 'code':0}
    return json.dumps(map)

@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.email_actived:
        return redirect('/')
    if current_user.confirm(token):
        flash('your account has been activated')
    else:
        flash('your account has not been activated, something error')
    return redirect('/')

