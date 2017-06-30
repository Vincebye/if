# -*- coding: UTF-8 -*-   
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask import request
import hashlib
import random
from . import db
from . import login_manager
from flask_login import UserMixin
import json
import uuid
import hashlib


class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1024))
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.Integer, default=0)  # 0 : normal, 1: deleted
    user = db.relationship('User')

    def __init__(self, content, image_id, user_id):
        self.content = content
        self.image_id = image_id
        self.user_id = user_id

    def __repr__(self):
        return '<Comment %d, content = %s, user_id = %s, image_id = %s, status = %d' % (self.id, self.content, self.user_id, self.image_id, self.status)

class Image(db.Model):
    __tablename__='images'
    id=db.Column(db.Integer,primary_key=True)
    url=db.Column(db.String(512))
    timestamp=db.Column(db.DateTime(),default=datetime.now)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    comments=db.relationship('Comment')

    def __init__(self,url,user_id):
        self.url = url
        self.user_id = user_id
        
    
    def __repr__(self):
        return '<Image %d, url = %s, user_id = %s, create_date = %s' % (self.id, self.url, self.user_id, self.timestamp)

class User(UserMixin,db.Model):
 

    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(50),unique=True)
    member_since=db.Column(db.DateTime(),default=datetime.now)
    password_hash=db.Column(db.String(128))
    images = db.relationship('Image', backref='user', lazy = 'dynamic')
    head_url = db.Column(db.String(256))  # 头像的url
    about_me=db.Column(db.Text())

    def __init__(self, email,username, password):
        self.username = username
        self.password = password
        self.email = email
        self.head_url = u'/static/yurisa/' + unicode(random.randint(0, 100)) + u'.jpg'
    
    def __repr__(self):
        return '%s'%(self.username)
    @property
    def is_authenticated(self):
        return True

    def is_admin(self):
        if self.username!='admin':
            return False
        else:
            return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
  
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
