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


t_stu_com = db.Table("table_stu_com",
                     db.Column("stu_id",db.String(20),db.ForeignKey("students.id"),primary_key=True),
                     db.Column("com_id",db.Integer,db.ForeignKey("Com_infos.id"),primary_key=True)
                     )


class Student(db.Model):  # 学生
    __tablename__ = 'students'
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    name = db.Column(db.String(20))
    dept = db.Column(db.String(20))
    age = db.Column(db.Integer)
    com_infos = db.relationship("Com_info", backref="students", secondary="table_stu_com")

    def __repr__(self):
        return '<student: %r>' % (self.name)

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
    def __str__(self):
        return 'Cominfo %s,%s,%s'%(self.name,self.holder,self.abstract)


class Holder(db.Model):  # 主办方
    __tablename__ = 'holders'
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    name = db.Column(db.String(20))


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
student1 = Student(id='new', password='123456', name='张伟康', dept='CS', age=22)
student2 = Student(id='gjj', password='123456', name='郭健健', dept='CS', age=23)
com_info1 = Com_info(name='程序设计大赛', sign_time='2019-04-01', start_time='2019-04-12', end_time='2019-04-13', holder='华为', abstract='星期五晚上8.30在信息馆有宣讲会')
com_info2 = Com_info(name='浙江省英语写作比赛',sign_time='2019-04-02',start_time='2019-04-04',end_time='2019-04-12',holder='生物学院',abstract='3.25号晚上在一号楼A401有宣讲会')
student1.com_infos.append(com_info2)
student2.com_infos.append(com_info1)
student2.com_infos.append(com_info2)
db.session.add(holder)
db.session.add(student1)
db.session.add(student2)
db.session.add(monitor)
db.session.add(com_info1)
db.session.add(com_info2)
db.session.commit()
print(student1.com_infos)
print(student2.com_infos)
print(com_info1.students)
print(com_info2.students)
if __name__ == '__main__':
    print('hello')
    app.run(debug=True)
