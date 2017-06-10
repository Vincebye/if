# -*- coding: UTF-8 -*-   
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask import request
import hashlib
from . import db
from . import login_manager
from flask_login import UserMixin
import json
import uuid
import hashlib

class Permission:
    FOLLOW=0x01
    COMMIT=0x02
    WRITE_ARTICLES=0x04
    MODERATE_COMMENTS=0x08
    ADMINISTER=0x80

PROFILE_FILE="profile.json"

class User(UserMixin,db.Model):
    # def __init__(self,**kwargs):
    #     super(User,self).__init__(**kwargs)
    #     if self.role is None:
    #         if self.email==current_app.config['FLASK_ADMIN']:
    #             self.role=Role.query.filter_by(permissions=0xff).first()
    #         if self.role is None:
    #             self.role=Role.query.filter_by(default=True).first()
               

    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(50),unique=True)
    location=db.Column(db.String(64))
    member_since=db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow)
    password_hash=db.Column(db.String(128))
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    about_me=db.Column(db.Text())
    avatar_hash=db.Column(db.String(32))

    @staticmethod
    def inser_user(email,username,password):
        user=User(email=email,username=username,password=password)
        db.session.add(user)
        db.session.commit()
    
    def __init__(self,**kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()
    def change_email(self,token):
        self.email=new_email
        self.avatar_hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True


#d 图画风格类型, 可选值有
#identicon 几何图形
#monsterid 怪兽
#wavatar 脸
#retro 8-bit
#f 当值为 y 时显示默认头像. 但当 d 有有效值时, f 失效.
#s 尺寸
#r 评级过滤


    def gravatar(self,size=100,default='monsterid',rating='g'):
        if request.is_secure:
            url='https://secure.gravatar.com/avatar'
        else:
            url='http://www.gravatar.com/avatar'
        hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)
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
class Role(UserMixin,db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True)
    default=db.Column(db.Boolean,default=False,index=True)
    permissions=db.Column(db.Integer)
    users=db.relationship('User',backref='role',lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles={
            'User':(Permission.FOLLOW|
                    Permission.COMMIT|
                    Permission.WRITE_ARTICLES,True),
            'Moderator':(Permission.FOLLOW|
                         Permission.COMMIT|
                         Permission.WRITE_ARTICLES|
                         Permission.MODERATE_COMMENTS,False),
            'Adminstrator':(0xff,False)
        }
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.permissions=roles[r][0]
            role.default=roles[r][1]
            db.session.add(role)
        db.session.commit()

class Picture(db.Model):
    __tablename__='pictures'
    id=db.Column(db.Integer,primary_key=True)
    url=db.Column(db.String(128))
    timestamp=db.Column(db.DateTime(),default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    @staticmethod
    def inser_picture(url,user_id):
        picture=Picture(url=url,user_id=user_id)
        db.session.add(picture)
        db.session.commit()
