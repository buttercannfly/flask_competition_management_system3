import random

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_login import LoginManager, current_user, login_user, login_required, UserMixin
import datetime

from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/flask_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 100  # 解决session连接的问题
db = SQLAlchemy(app)
login_manager = LoginManager()  # 创建LoginManager实例.
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)
app.secret_key = 'random string'
# SQLALCHEMY_POOL_SIZE = 100
# engine = create_engine('mysql+pymysql://root:123@localhost/flask_demo',
#                            pool_recycle=10600, pool_size=100, max_overflow=20)
create_engine.pool_size = 100


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
                     db.Column("stu_id", db.String(20), db.ForeignKey("students.id"), primary_key=True),
                     db.Column("com_id", db.Integer, db.ForeignKey("Com_infos.id"), primary_key=True),
                     db.Column("grade", db.String(20))
                     )

t_team_stu = db.Table("table_team_stu",
                      db.Column("stu_id", db.String(20), db.ForeignKey("students.id"), primary_key=True),
                      db.Column("team_id", db.Integer, db.ForeignKey("teams.id"), primary_key=True),
                      )
t_com_team = db.Table(
    "table_com_team",
    db.Column("com_id", db.Integer, db.ForeignKey("Com_infos.id"), primary_key=True),
    db.Column("team_id", db.Integer, db.ForeignKey("teams.id"), primary_key=True),
    db.Column("grade", db.String(20))
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


class Team(db.Model):  # 队伍
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    students = db.relationship('Student', backref='teams', secondary="table_team_stu")

    def __repr__(self):
        return '<team: %r>' % (self.id)


class Com_info(db.Model):  # 竞赛信息
    __tablename__ = 'Com_infos'
    name = db.Column(db.String(20))
    holder = db.Column(db.String(20))
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    sign_time = db.Column(db.Date)
    start_time = db.Column(db.Date)
    put_time = db.Column(db.Date)  # 发布时间
    com_level = db.Column(db.String(20))  # 竞赛等级
    org_party = db.Column(db.String(20))  # 组织单位
    com_place = db.Column(db.String(20))  # 竞赛地点
    teacher = db.Column(db.String(20))  # 指导教师
    end_time = db.Column(db.Date)
    abstract = db.Column(db.String(200))
    award = db.Column(db.String(40))
    assign = db.Column(db.String(20))
    pattern = db.Column(db.String(20))  # 参赛人数
    min_p = db.Column(db.Integer)
    max_p = db.Column(db.Integer)
    teams = db.relationship('Team', backref='Com_infos', secondary="table_com_team")

    def __repr__(self):
        return '<Cominfo %r>' % (self.name)

    def __str__(self):
        return 'Cominfo %s,%s,%s' % (self.name, self.holder, self.abstract)


class Holder(db.Model):  # 主办方
    __tablename__ = 'holders'
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    name = db.Column(db.String(20))


class Notice(db.Model):  # 通知公告
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    put_time = db.Column(db.Date)
    author = db.Column(db.String(20))
    source = db.Column(db.String(20))
    dept = db.Column(db.String(20))
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Notice:%s>' % (self.name)


class Teacher(db.Model):  # 老师
    __tablename__ = 'teachers'
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    name = db.Column(db.String(20), unique=True)
    academic = db.Column(db.String(20))
    email = db.Column(db.String(20))

    # students = db.relationship('Student', backref='teacher', lazy='dynamic')

    def __repr__(self):
        return '<Teacher:%s>' % (self.name)


db.drop_all()
db.create_all()
monitor = Monitor(id='butter', password='123456')
holder = Holder(id='ztgt', password='123456', name='中天钢铁')
student1 = Student(id='zwk', password='123456', name='张伟康', dept='计算机学院', age=22)
student2 = Student(id='gjj', password='123456', name='郭健', dept='管理学院', age=23)
student3 = Student(id='xiaoyun', password='123456', name='肖云', dept='计算机学院', age=23)
student4 = Student(id='zhangjx', password='123456', name='张佳祥', dept='计算机学院', age=23)
student5 = Student(id='hantianzhu', password='123456', name='韩天柱', dept='计算机学院', age=23)
student6 = Student(id='zhangsan', password='123456', name='张三', dept='理学院', age=24)
student7 = Student(id='lisi', password='123456', name='张四', dept='理学院', age=24)
student8 = Student(id='wanger', password='123456', name='王二', dept='理学院', age=24)
student9 = Student(id='liuliu', password='123456', name='刘留', dept='建筑学院', age=22)
student10 = Student(id='kankang', password='123456', name='刘洪', dept='信息科学与技术学院', age=23)
student11 = Student(id='kankang1', password='123456', name='刘闯', dept='信息科学与技术学院', age=23)
student12 = Student(id='kankang2', password='123456', name='刘刘', dept='信息科学与技术学院', age=23)
student13 = Student(id='kankang3', password='123456', name='刘宝', dept='信息科学与技术学院', age=23)
com_info1 = Com_info(name='程序设计大赛', sign_time='2019-04-01', start_time='2019-04-12', end_time='2019-04-13', holder='华为',
                     com_place='校内', com_level='省级', org_party='华为校园部', put_time='2019-03-12', teacher='赵四',
                     pattern='个人',
                     abstract='星期五晚上8.30在信息馆有宣讲会', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info2 = Com_info(name='浙江省英语写作比赛', sign_time='2019-05-28', start_time='2019-05-29', end_time='2019-05-30',
                     com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', pattern='1-4',
                     teacher='肖桐 马冬梅',
                     holder='生物学院', abstract='3.25号晚上在一号楼A401有宣讲会', award='优胜奖', assign='1')
com_info3 = Com_info(name='浙江省大学生证券投资竞赛', sign_time='2019-06-07', start_time='2019-06-12',
                     com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', pattern='个人',
                     teacher='肖桐 马冬梅',
                     end_time='2019-06-14', abstract='', holder='金融学院', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info4 = Com_info(name='浙江省大学生管理案例竞赛', sign_time='2019-04-22', start_time='2019-03-24', pattern='1-4',
                     com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                     end_time='2019-06-30', abstract='', holder='管理学院', award='一等奖 二等奖 三等奖',assign='1 1 1')
com_info5 = Com_info(name='浙江省大学生汉语口语竞赛', sign_time='2019-03-23', start_time='2019-03-29', pattern='个人',
                     com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                     end_time='2019-04-01', abstract='', holder='基础教学部', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info6 = Com_info(name='浙江省体育产业创新创业大赛', sign_time='2019-03-23', start_time='2019-03-29', pattern='个人',
                     com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                     end_time='2019-04-01', abstract='', holder='团委', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info7 = Com_info(name='浙江省大学生摄影大赛', sign_time='2019-03-23', start_time='2019-04-29', pattern='个人',
                     com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                     end_time='2019-06-01', abstract='', holder='艺术设计学院', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info8 = Com_info(name='浙江省大学生广告艺术设计大赛', sign_time='2019-04-25', start_time='2019-04-29', pattern='个人',
                     com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                     end_time='2019-05-01', abstract='', holder='艺术设计学院', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info9 = Com_info(name='浙江省大学生职业生涯规划大赛', sign_time='2019-04-25', start_time='2019-04-29', pattern='个人',
                     com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                     end_time='2019-05-01', abstract='', holder='就业处', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info10 = Com_info(name='浙江省挑战杯大学生课外学术科技作品竞赛', sign_time='2019-05-08', start_time='2019-05-10', pattern='个人',
                      com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                      end_time='2019-05-12', abstract='', holder='挑战杯', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info11 = Com_info(name='浙江省挑战杯大学生化工设计竞赛', sign_time='2019-05-08', start_time='2019-05-10', pattern='个人',
                      com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                      end_time='2019-05-12', abstract='', holder='挑战杯', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info12 = Com_info(name='浙江省挑战杯大学生英语演讲竞赛', sign_time='2019-05-08', start_time='2019-05-10', pattern='个人',
                      com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                      end_time='2019-05-12', abstract='', holder='挑战杯', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info13 = Com_info(name='浙江省挑战杯大学生财会信息化竞赛', sign_time='2019-05-08', start_time='2019-05-10', pattern='个人',
                      com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                      end_time='2019-05-12', abstract='', holder='挑战杯', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info14 = Com_info(name='浙江省挑战杯大学生教学技能竞赛', sign_time='2019-05-08', start_time='2019-05-10', pattern='个人',
                      com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                      end_time='2019-05-12', abstract='', holder='挑战杯', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info15 = Com_info(name='浙江省挑战杯大学生多媒体作品竞赛', sign_time='2019-05-08', start_time='2019-05-10', pattern='个人',
                      com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                      end_time='2019-05-12', abstract='', holder='挑战杯', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info16 = Com_info(name='浙江省挑战杯大学生机械设计竞赛', sign_time='2019-05-08', start_time='2019-05-10', pattern='个人',
                      com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                      end_time='2019-05-12', abstract='', holder='挑战杯', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info17 = Com_info(name='浙江省挑战杯大学生电子设计竞赛', sign_time='2019-05-11', start_time='2019-05-12', pattern='个人',
                      com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                      end_time='2019-05-12', abstract='', holder='挑战杯', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info18 = Com_info(name='浙江省挑战杯大学生程序设计竞赛', sign_time='2019-05-11', start_time='2019-05-12', pattern='个人',
                      com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                      end_time='2019-05-12', abstract='', holder='挑战杯', award='一等奖 二等奖 三等奖', assign='1 1 1')
com_info19 = Com_info(name='浙江省挑战杯大学生大学生创新创业竞赛', sign_time='2019-05-11', start_time='2019-05-11', pattern='个人',
                      com_place='校内', com_level='省级', org_party='教务处', put_time='2019-03-12', teacher='肖桐 马冬梅',
                      end_time='2019-05-12', abstract='', holder='挑战杯', award='一等奖 二等奖 三等奖', assign='1 1 1')
teacher1 = Teacher(id='xiaotong',
                   password='123456',
                   name='肖桐',
                   academic='计算机学院',
                   email='1710085142@qq.com')
team1 = Team()
team1.students.append(student2)
team1.students.append(student4)
team1.students.append(student5)
team2 = Team()
team2.students.append(student3)
team2.students.append(student6)
team3 = Team()
team3.students.append(student7)
team3.students.append(student8)
team3.students.append(student9)
com_info2.teams.append(team1)
com_info2.teams.append(team2)
com_info2.teams.append(team3)

team4 = Team()
team5 = Team()
team6 = Team()
team4.students.append(student2)
team4.students.append(student4)
team4.students.append(student5)
team5.students.append(student3)
team5.students.append(student6)
team6.students.append(student7)
team6.students.append(student8)
team6.students.append(student9)
com_info4.teams.append(team4)
com_info4.teams.append(team5)
com_info4.teams.append(team6)
db.session.commit()
student2.com_infos.append(com_info2)
student2.com_infos.append(com_info4)
student3.com_infos.append(com_info2)
student3.com_infos.append(com_info4)
student4.com_infos.append(com_info2)
student4.com_infos.append(com_info4)
student5.com_infos.append(com_info2)
student5.com_infos.append(com_info4)
student6.com_infos.append(com_info2)
student6.com_infos.append(com_info4)
student7.com_infos.append(com_info2)
student7.com_infos.append(com_info4)
student8.com_infos.append(com_info2)
student8.com_infos.append(com_info4)
student9.com_infos.append(com_info2)
student9.com_infos.append(com_info4)

# student1.com_infos.append(com_info2)
student1.com_infos.append(com_info1)
# student1.com_infos.append(com_info4)
student1.com_infos.append(com_info5)
student1.com_infos.append(com_info6)
student1.com_infos.append(com_info11)
student1.com_infos.append(com_info12)
student1.com_infos.append(com_info15)
student1.com_infos.append(com_info16)
student1.com_infos.append(com_info17)
student2.com_infos.append(com_info1)
# student2.com_infos.append(com_info2)
# student2.com_infos.append(com_info4)
student2.com_infos.append(com_info6)
student2.com_infos.append(com_info8)
student2.com_infos.append(com_info9)
student2.com_infos.append(com_info11)
student2.com_infos.append(com_info12)
student2.com_infos.append(com_info14)
student2.com_infos.append(com_info16)
student2.com_infos.append(com_info18)
student2.com_infos.append(com_info19)
# student3.com_infos.append(com_info2)
student3.com_infos.append(com_info1)
# student3.com_infos.append(com_info4)
student3.com_infos.append(com_info5)
student3.com_infos.append(com_info7)
student3.com_infos.append(com_info12)
student3.com_infos.append(com_info11)
student3.com_infos.append(com_info14)
student3.com_infos.append(com_info15)
student3.com_infos.append(com_info17)
# student4.com_infos.append(com_info2)
student4.com_infos.append(com_info1)
# student4.com_infos.append(com_info4)
student4.com_infos.append(com_info5)
student4.com_infos.append(com_info7)
student4.com_infos.append(com_info12)
student4.com_infos.append(com_info11)
student4.com_infos.append(com_info14)
student4.com_infos.append(com_info15)
student4.com_infos.append(com_info17)
student5.com_infos.append(com_info3)
# student5.com_infos.append(com_info2)
student5.com_infos.append(com_info6)
student5.com_infos.append(com_info8)
student5.com_infos.append(com_info9)
student5.com_infos.append(com_info13)
student5.com_infos.append(com_info12)
student5.com_infos.append(com_info16)
student5.com_infos.append(com_info18)
student5.com_infos.append(com_info19)
student6.com_infos.append(com_info3)
# student6.com_infos.append(com_info4)
student6.com_infos.append(com_info5)
student6.com_infos.append(com_info7)
student6.com_infos.append(com_info9)
student6.com_infos.append(com_info13)
student6.com_infos.append(com_info14)
student6.com_infos.append(com_info15)
student6.com_infos.append(com_info17)
student6.com_infos.append(com_info19)
student7.com_infos.append(com_info3)
# student7.com_infos.append(com_info4)
student7.com_infos.append(com_info5)
student7.com_infos.append(com_info7)
student7.com_infos.append(com_info9)
student7.com_infos.append(com_info13)
student7.com_infos.append(com_info14)
student7.com_infos.append(com_info15)
student7.com_infos.append(com_info17)
student7.com_infos.append(com_info19)

student8.com_infos.append(com_info1)
# student8.com_infos.append(com_info2)
student8.com_infos.append(com_info10)
student8.com_infos.append(com_info6)
student8.com_infos.append(com_info8)
student8.com_infos.append(com_info11)
student8.com_infos.append(com_info12)
student8.com_infos.append(com_info15)
student8.com_infos.append(com_info16)
student8.com_infos.append(com_info18)

# student9.com_infos.append(com_info2)
student9.com_infos.append(com_info10)
# student9.com_infos.append(com_info4)
student9.com_infos.append(com_info6)
student9.com_infos.append(com_info8)
student9.com_infos.append(com_info1)
student9.com_infos.append(com_info3)
student9.com_infos.append(com_info5)
student9.com_infos.append(com_info7)
student9.com_infos.append(com_info9)

student10.com_infos.append(com_info3)
# student10.com_infos.append(com_info4)
student10.com_infos.append(com_info5)
student10.com_infos.append(com_info7)
student10.com_infos.append(com_info9)
student10.com_infos.append(com_info13)
student10.com_infos.append(com_info14)
student10.com_infos.append(com_info15)
student10.com_infos.append(com_info17)
student10.com_infos.append(com_info19)

student11.com_infos.append(com_info3)
# student11.com_infos.append(com_info4)
student11.com_infos.append(com_info5)
student11.com_infos.append(com_info7)
student11.com_infos.append(com_info9)
student11.com_infos.append(com_info13)
student11.com_infos.append(com_info14)
student11.com_infos.append(com_info15)
student11.com_infos.append(com_info17)
student11.com_infos.append(com_info19)

student12.com_infos.append(com_info1)
# student12.com_infos.append(com_info2)
# student12.com_infos.append(com_info4)
student12.com_infos.append(com_info6)
student12.com_infos.append(com_info8)
student12.com_infos.append(com_info9)
student12.com_infos.append(com_info11)
student12.com_infos.append(com_info12)
student12.com_infos.append(com_info14)
student12.com_infos.append(com_info16)
student12.com_infos.append(com_info18)
student12.com_infos.append(com_info19)

# student13.com_infos.append(com_info2)
student13.com_infos.append(com_info1)
# student13.com_infos.append(com_info4)
student13.com_infos.append(com_info5)
student13.com_infos.append(com_info7)
student13.com_infos.append(com_info12)
student13.com_infos.append(com_info11)
student13.com_infos.append(com_info14)
student13.com_infos.append(com_info15)
student13.com_infos.append(com_info17)

notice1 = Notice(name='第二届全国高校企业价值创造实战竞赛校内选拔赛顺利举办',
                 put_time='2019-04-11',
                 author='肖桐',
                 source='创新创业中心',
                 dept='计算机学院',
                 content='3月22日，我院在J709顺利举办第二届全国高校企业价'
                         '值创造实战竞赛校内选拔赛，第二届全国高校企业价值创造实战竞赛是由教育部会'
                         '计学专业教学指导分委员会启动的竞赛活动，赛事分为三个阶段：校内赛、区域赛、总决赛。'
                         '校内选拔赛中，参赛学生分别担任企业的CEO、财务总监、运营总监、市场总监，进行模拟经营实战'
                         '比拼，在三个小时内完成6期经营，李沛尧、于雷、李卓远、张启尧获得一等奖，范一波、张馨月、周静怡、傅东辰获得二等奖。')
notice2 = Notice(name='纳入学科竞赛排行的竞赛项目',
                 put_time='2018-09-28',
                 author='肖桐',
                 source='创新创业中心',
                 dept='计算机学院',
                 content='1中国“互联网+”大学生创新创业大赛'
                         '2“挑战杯”全国大学生课外学术科技作品竞赛'
                         '3“创青春”中国大学生创业计划大赛'
                         '4ACM-ICPC国际大学生程序设计竞赛'
                         '5全国大学生数学建模竞赛'
                         '6全国大学生电子设计竞赛'
                         '7全国大学生化学实验邀请赛'
                         '8全国高等医学院校大学生临床技能竞赛'
                         '9全国大学生机械创新设计大赛'
                         '10全国大学生结构设计竞赛'
                         '11全国大学生广告艺术大赛'
                         '12全国大学生智能汽车竞赛'
                         '13全国大学生交通科技大赛'
                         '14全国大学生电子商务“创新、创意及创业”挑战赛'
                         '15全国大学生节能减排社会实践与科技竞赛'
                         '16全国大学生工程训练综合能力竞赛'
                         '17全国大学生物流设计大赛'
                         '18“外研社杯”全国英语演讲大赛'
                         '19全国职业院校技能大赛')
notice3 = Notice(name='关于2019年第十二届全国周培源大学生力学竞赛暨第十一届江苏省大学生力学竞赛校内选拔赛考试安排的通知',
                 put_time='2019-03-13',
                 author='肖桐',
                 source='创新创业中心',
                 dept='计算机学院',
                 content='各学院：根据3月1日发布的《关于举办2019年第十二届全国'
                         '周培源大学生力学竞赛暨第十一届江苏省大学生力学竞赛校内'
                         '选拔赛的通知》，本次选拔赛如期举行。请相关学院通知学生携'
                         '带一卡通（或身份证）参加选拔考试，考试时间：3月16日（本周'
                         '六）上午8：30- 12：00，教室和名单见附件。如有疑问， 请咨询'
                         '创新创业教育中心，吴老师、任老师，联系电话：025-58731344。')
notice4 = Notice(name='2018-2019学年第二学期藕舫学院地面气象观测实验班（“观云测天”实践计划）报名选拔通知',
                 put_time='2019-04-12',
                 author='创新创业教育中心',
                 source='创新创业教育中心',
                 dept='大气与环境实验教学中心',
                 content='各学院：为进一步贯彻落实我校创新人才培养理念和实践人才培养目标'
                         '，充分发挥中国气象局综合观测培训实习基地（南京）和专业实验室的功'
                         '能，加大实验教学平台的开放力度，加强我校学生实践能力和创新精神的'
                         '培养，在教务处、研究生院等学校相关部门的支持下，拟招收地面气象观测'
                         '实验班（“观云测天”实践计划）核心成员。学员两学期的实践计划结束，'
                         '经综合测评合格，可获得2个学分，按《地面气象观测当班实习》选修课程'
                         '计入学生成绩档案，同时颁发南京信息工程大学“观云测天”实践计划证书'
                         '。现将开班报名选拔工作等有关事项通知如下：1.  报名对象 在校全日制大'
                         '气科学类及相关专业本科生（二年级及以上），拟招收核心成员90人。2．选拔'
                         '条件 （1）学习勤奋，基础扎实，修读完或在修《大气探测学》和《大气探测实'
                         '习》专业课程，成绩优良； （2）思维敏捷，积极实践，勇于创新，有钻研精神'
                         '和自学能力； （3）吃苦耐劳，具有高度的责任感、团队意识和敬业精神；（4）'
                         '对地面气象观测、探测技术和气象业务拥有浓厚兴趣者优先。 3. 选拔流程（1）'
                         '学生自愿报名，进行面试（面试时间在报名截止后一周内另行通知）； 2）对拟接'
                         '纳成员名单进行公示。 4. 报名时间及方式3月19日16:00前，在教务处主页（http'
                         '://jwc.nuist.edu.cn/）点击右下角“实践教学综合管理平台”，登录“学科竞赛'
                         '管理系统”（用户名和初始密码均为学号）→选择“地面气象观测实验班（“观云'
                         '测天”实践计划）”报名→填写联系方式等。注：面试时请携带打印的个人电子报名'
                         '表（附照片）研究生院、滨江学院的如需报名可下载个人电子报名表，填写报名表后'
                         '打印交至中国气象局综合观测培训实习基地（南京）（南京信息工程大学大探基地）'
                         '104室。联系人：吴老师；电话：18795803392。')
# notice5 = Notice(name=)

db.session.add(notice1)
db.session.add(notice2)
db.session.add(notice3)
db.session.add(notice4)
db.session.add(teacher1)
db.session.add(holder)
db.session.add(student1)
db.session.add(student2)
db.session.add(student3)
db.session.add(student4)
db.session.add(student5)
db.session.add(student6)
db.session.add(student7)
db.session.add(monitor)
db.session.add(com_info1)
db.session.add(com_info2)
db.session.add(com_info3)
db.session.add(com_info4)
db.session.add(com_info5)
db.session.add(com_info6)
db.session.add(com_info7)
db.session.add(com_info8)
db.session.add(com_info9)
db.session.add(com_info11)
db.session.add(com_info12)
db.session.add(com_info13)
db.session.add(com_info14)
db.session.add(com_info15)
db.session.add(com_info16)
db.session.add(com_info17)
db.session.add(com_info18)
db.session.add(com_info19)
db.session.add(com_info10)
db.session.commit()
com_infos = Com_info.query.all()
today = datetime.date.today()
# print(today)
for com_info in com_infos:
    if com_info.sign_time >= today:
        com_info.status = 1
        db.session.commit()
    elif com_info.start_time <= today <= com_info.end_time:
        com_info.status = 2
        db.session.commit()
    elif com_info.end_time <= today:
        com_info.status = 0
        stu_lists = com_info.students
        for stu_list in stu_lists:
            award_list = com_info.award.split()
            award_temp = award_list[random.randint(0, len(award_list) - 1)]
            sql = "UPDATE table_stu_com SET grade = '%s' WHERE stu_id = '%s' AND com_id = '%s'" % (
                award_temp, stu_list.id, com_info.id)
            db.session.execute(sql)
        db.session.commit()
    else:
        com_info.status = 3
        db.session.commit()
    db.session.commit()


class Admin(db.Model, UserMixin):
    __tablename = 'admin'
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))

    def is_active(self):  # line 37
        return True

    def __init__(self, id, password):
        self.id = id
        self.password = password

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Admin %r>' % self.id


@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))


admin1 = Admin(id='zwk', password='123456')
db.session.add(admin1)
db.session.commit()
db.session.close()
# print(student1.com_infos)
# print(student2.com_infos)
# print(com_info1.students)
# print(com_info2.students)
if __name__ == '__main__':
    print('hello')
    app.run(debug=True)
