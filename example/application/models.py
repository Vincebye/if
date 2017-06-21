# -*- coding:utf8 -*-

from application import db, login_manager
from datetime import datetime
import random
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, default=0)  # 0 : normal, 1: deleted
    user = db.relationship('User')

    def __init__(self, content, image_id, user_id):
        self.content = content
        self.image_id = image_id
        self.user_id = user_id

    def __repr__(self):
        return '<Comment %d, content = %s, user_id = %s, image_id = %s, status = %d' % (self.id, self.content, self.user_id, self.image_id, self.status)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_date = db.Column(db.String(128))
    comments = db.relationship('Comment')

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return '<Image %d, url = %s, user_id = %s, create_date = %s' % (self.id, self.url, self.user_id, self.create_date)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    salt = db.Column(db.String(32))
    head_url = db.Column(db.String(256))  # 头像的url
    images = db.relationship('Image', backref='user', lazy = 'dynamic')
    email_actived = db.Column(db.BOOLEAN, default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.email_actived = True
        db.session.add(self)
        db.session.commit()
        return True


    #images = db.relationship('Image')

    @property
    def is_authenticated(self):
        print 'is_authenticated'
        return True

    @property
    def is_active(self):
        print 'is_active'
        return True

    def is_anonymous(self):
        print 'is_anonymous'
        return False

    def get_id(self):
        print 'get_id'
        return self.id
        #return unicode(id)

    def __init__(self, username, email, password, salt = ''):
        self.username = username
        self.password = password
        self.email = email
        self.salt = salt
        self.head_url = u'/static/yurisa/' + unicode(random.randint(0, 100)) + u'.jpg'

    def __repr__(self):
        return '<User %d, name = %s, password = %s, head_url = %s' % (self.id, self.username, self.password, self.head_url)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)