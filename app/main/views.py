# -*- coding:utf8 -*-

from flask import request,render_template,redirect,url_for,flash,abort,jsonify
from .forms import EditProfileForm,EditProfileAdminForm
from . import main
from .. import db
from .. import pictures
from ..models import User,Image,Comment
from flask_wtf.csrf import CsrfProtect
import os
from flask_login import login_user,login_required,LoginManager,current_user,logout_user
basedir=os.path.abspath(os.path.dirname(__file__))

#首页
@main.route("/")
def index():
    images=Image.query.order_by('id desc').paginate(1,5,False)
    return render_template('index.html',images=images.items)

# 首页ajax 的json 数据
@main.route('/images/<int:page_num>/<int:per_page>/')
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
    print 'sad\n'
    return jsonify(map)


@main.route("/upload",methods=['POST','GET'])
@login_required
def upload():
    if request.method=='POST' and 'picture' in request.files:
        filename = pictures.save(request.files['picture'],folder='./upload')
        fileurl=pictures.url(filename)
        pic=Image(url=fileurl,user_id=current_user.id)
        db.session.add(pic)
        db.session.commit()
    return redirect(url_for('main.profile',id=current_user.id))

# 图片详情页
@main.route('/image/<int:id>/')
def image(id):
    images = Image.query.get(id)
    if images == None:
        return redirect('/')
    return render_template('pageDetail.html', images = images)


   
# @main.route("/user/<username>")
# def show_user_profile(username):
#     user=User.query.filter_by(username=username).first()
#     if user is None:
#         abort(404)
#     return render_template('user.html',user=user)

# 个人详情页
@main.route('/profile/<int:id>/')
@login_required
def profile(id):
    user = User.query.get(id)
    if user == None:
        return redirect('/')
    images = user.images.paginate(1, 6, False)
    return render_template('profile.html', user = user, images = images.items, has_next = images.has_next)

# 个人详情页 ajax 数据
@main.route('/profile/images/<int:id>/<int:page_num>/<int:per_page>/')
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
    return jsonify(map)

#添加评论
@main.route('/addcomment/', methods=['POST'])
@login_required
def addcomment():
    image_id = int(request.values['image_id'])
    content = request.values['content'].strip()
    comment = Comment(content, image_id, current_user.id)
    db.session.add(comment)
    db.session.commit()
    map = {'user_id':current_user.id, 'username' : current_user.username, 'code':0}
    return jsonify(map)

# @main.route("/edit-profile",methods=['GET','POST'])
# @login_required
# def edit_profile():
#     form=EditProfileForm()
#     if form.validate_on_submit():
#         current_user.username=form.username.data
#         current_user.location=form.location.data
#         current_user.about_me=form.about_me.data
#         db.session.add(current_user)
#         flash('Your profile has been updated')
#         return redirect(url_for('.user',username=current_user.username))
#     form.username.data=current_user.username
#     form.location.data=current_user.location
#     form.about_me.data=current_user.about_me
#     return render_template('edit_profile.html',form=form)

# @main.route("/edit-profile/<int:id>",methods=['GET','POST'])
# @login_required
# @admin_required
# def edit_profile_admin(id):
#     user=User.query.get_or_404(id)
#     form=EditProfileAdminForm(user=user)
#     if form.validate_on_submit():
#         user.email=form.email.data
#         user.username=form.username.data
#         user.role=Role.query.get(form.role.data)
#         user.location=form.location.data
#         user.about_me=form.about_me.data
#         db.session.add(user)
#         db.session.commit()
#         flash("The profile has been updated")
#         return redirect(url_for('.user',username=user.username))
#     form.email.data=user.email
#     form.username.data=user.username
#     form.role.data=user.role_id
#     form.location.data=user.location
#     form.about_me.data=user.about_me
#     return render_template('edit_profile.html',form=form,user=user)
