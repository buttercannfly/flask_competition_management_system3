from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/flask_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Monitor(db.Model):  # 管理员
    __tablename__ = 'monitors'
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))

    def __init__(self, id, password):
        self.password = password
        self.id = id

    def __repr__(self):
        return '<User %r>' % self.id


class Student(db.Model):  # 学生
    __tablename__ = 'students'
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    name = db.Column(db.String(20))
    dept = db.Column(db.String(20))
    age = db.Column(db.Integer)


# class Teacher(db.Model):
#     __tablename__ = 'teachers'
#     id = db.Column(db.String(20), primary_key=True)
#
class Holder(db.Model):  # 主办方
    __tablename__ = 'holders'
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    name = db.Column(db.String(20))


class Com_info(db.Model):  # 竞赛信息
    __tablename__ = 'Com_infos'
    name = db.Column(db.String(20))
    holder = db.Column(db.String(20))
    id = db.Column(db.Integer, primary_key=True)
    sign_time = db.Column(db.String(20))
    start_time = db.Column(db.String(20))
    end_time = db.Column(db.String(20))
    abstract = db.Column(db.String(200))

    def __repr__(self):
        return '<Cominfo %r>' % (self.name)


class Notice(db.Model):  # 通知公告
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True)
    hold = db.Column(db.String(20))
    title = db.Column(db.String(20))
    content = db.Column(db.String(80))
    span_time = db.Column(db.String(20))
    status = db.Column(db.Boolean)


db.drop_all()
db.create_all()
monitor = Monitor(id='nut', password='123456')
holder = Holder(id='but', password='123456', name='中天钢铁')
student = Student(id='new', password='123456', name='张伟康', dept='CS', age=22)
com_info = Com_info(name='程序设计大赛', sign_time='2019-04-01', start_time='2019-04-12', end_time='2019-04-13', holder='华为')
db.session.add(holder)
db.session.add(student)
db.session.add(monitor)
db.session.add(com_info)
db.session.commit()
if __name__ == '__main__':
    print('hello')
    app.run(debug=True)
