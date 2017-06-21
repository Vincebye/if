# -*- coding:utf8 -*-

from application import app, db
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from application.models import User, Image, Comment
from sqlalchemy import or_, and_
import random

manager = Manager(app)

def getImageUrl():
    return u'/static/yurisa/' + unicode(random.randint(0, 100)) + u'.jpg'

@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 30):
        db.session.add(User(u'User' + unicode(i), 'admin' + unicode(i) + '@qq.com', u'password' + unicode(i)))
        for j in range(0, 3):
            db.session.add(Image(getImageUrl(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment(u'This is a comment' + unicode(k), 3 * i + j + 1, i + 1))
    db.session.commit()

    for i in range(1, 15, 2):
        user = User.query.get(i)
        #print user
        user.username = u'[New]' + user.username
    db.session.commit()

    User.query.filter_by(id = 1).update({'username':'[new 2]'})
    db.session.commit()

    # for i in range(1, 15, 2):
    #     comment = Comment.query.get(i)
    #     db.session.delete(comment)
    # db.session.commit()

    print 1, User.query.all()
    print 2, User.query.get(3)
    print 3, User.query.filter_by(id=5).first()
    print 4, User.query.order_by(User.id.desc()).offset(1).limit(2).all()
    print 5, User.query.filter(User.username.endswith('0')).limit(3).all()
    print 6, User.query.filter(or_(User.id == 12, User.id == 19)).all()
    print 7, User.query.filter(and_(User.id > 12, User.id < 29)).all()
    print 8, User.query.filter(and_(User.id > 12, User.id < 29)).first_or_404()
    # 分页
    print 9, User.query.paginate(page = 1, per_page = 10).items
    # 一对多查询
    user = User.query.get(1)
    print 10, user.images
    image = Image.query.get(1)
    print 11, image

if __name__ == '__main__':
    manager.run()
