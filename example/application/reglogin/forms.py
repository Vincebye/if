# -*- coding:utf8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Email, EqualTo
from application.models import User

class LoginForm(Form):
    username = StringField(u'用户名', validators=[Required(), Length(1, 32)])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'登陆')

class RegisterForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[Required(), Length(1, 32)])
    password = PasswordField(u'密码', validators=[Required()])
    password_confirm = PasswordField(u'确认密码', validators=[Required(), EqualTo('password', u'密码不一致')])
    submit = SubmitField(u'注册')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已经被注册')
