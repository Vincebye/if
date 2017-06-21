from flask import request,render_template,redirect,url_for,flash,abort,jsonify
from .forms import EditProfileForm,EditProfileAdminForm
from . import main
from .. import db
from .. import pictures
from ..models import User,Role,Picture
from flask_wtf.csrf import CsrfProtect
import os
from flask_login import login_user,login_required,LoginManager,current_user,logout_user
basedir=os.path.abspath(os.path.dirname(__file__))
from ..decorators import admin_required, permission_required

@main.route("/")
def index():
    url_list=[]
    picture=Picture.query.limit(2).all()
    for i in picture:
        url_list.append(i.url)
    return render_template('index.html',url_list=url_list)

@main.route("/user/<username>")
def show_user_profile(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)

@main.route("/edit-profile",methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.location=form.location.data
        current_user.about_me=form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated')
        return redirect(url_for('.user',username=current_user.username))
    form.username.data=current_user.username
    form.location.data=current_user.location
    form.about_me.data=current_user.about_me
    return render_template('edit_profile.html',form=form)

@main.route("/edit-profile/<int:id>",methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user=User.query.get_or_404(id)
    form=EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email=form.email.data
        user.username=form.username.data
        user.role=Role.query.get(form.role.data)
        user.location=form.location.data
        user.about_me=form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash("The profile has been updated")
        return redirect(url_for('.user',username=user.username))
    form.email.data=user.email
    form.username.data=user.username
    form.role.data=user.role_id
    form.location.data=user.location
    form.about_me.data=user.about_me
    return render_template('edit_profile.html',form=form,user=user)

@main.route("/upload",methods=['POST','GET'])
@login_required
def upload():
    if request.method=='POST' and 'picture' in request.files:
        filename = pictures.save(request.files['picture'],folder='./upload')
        fileurl=pictures.url(filename)
        pic=Picture(url=fileurl,user_id=current_user.id)
        db.session.add(pic)
        db.session.commit()
        #return 'sdadd'
        #return redirect(url_for('show', name=filename))
    return render_template('upload.html')

@main.route("/picture/<int:id>",methods=['POST','GET'])
def show(id):
    if name is None:
        abort(404)
@main.route("/json",methods=['POST','GET'])
def json():
    try:
        print data
    except:
        pass
    print '++++++'
    return jsonify(hits=3123123)
    
