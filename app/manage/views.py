# -*- coding: UTF-8 -*-  
from .. import admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin,BaseView,expose
import os.path as op
from .. import db
from flask_login import login_user,login_required,LoginManager,current_user
from ..models import User,Image,Comment

#后台管理页面
class MicroBlogModelView(ModelView):

    def is_accessible(self):
        return current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

class MyAdminIndexView(BaseView):
    @expose('/',methods=['GET', 'POST'])
    @login_required
    def index(self):
        return self.render('admin/index.html')
    
    @expose('/admin',methods=['GET', 'POST'])
    @login_required
    def index(self):
        return self.render('admin/index.html')

class UserView(ModelView):
    #自定义显示的columns名字
    column_labels=dict(
        username=u'用户名',
        email=u'电子邮件',
        password_hash=u'密码',
        head_url=u'头像链接'
    )

    #定义不想显示的字段
    column_exclude_list=(
        'location',
        'last_seen',
        'head url',
        'about_me',
        'avatar_hash',
        'role'
    )

class ImageView(ModelView):
    #自定义显示的columns名字
    column_labels=dict(
        url=u'图片链接',
        timestamp=u'时间戳',
    )

    #定义不想显示的字段
    column_exclude_list=(
        
    )

class CommentView(ModelView):
    #自定义显示的columns名字
    column_labels=dict(
        content=u'评论内容',
    )

    #定义不想显示的字段
    column_exclude_list=(
        'status'
    )

admin.add_view(UserView(User,db.session,name=u'用户'))
admin.add_view(ImageView(Image,db.session,name=u'图片'))
admin.add_view(CommentView(Comment,db.session,name=u'评论'))


path=op.join(op.dirname(__file__),'../../upload')
admin.add_views(FileAdmin(path,'/upload',name='Image File'))



