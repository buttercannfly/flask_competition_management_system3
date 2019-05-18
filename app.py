import random

from flask import Flask, render_template, redirect, url_for, request, flash, g, current_app
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from wtforms import Form, TextField, PasswordField, validators
import hello
import datetime
import os
import re
import __init__
from __init__ import *
from hello import *
import json
import sys
from os import path

__init__
hello  # 调用hello初始化模板
app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = '123456'
# app.secret_key = ''
bootstrap = Bootstrap(app)
app.debug = True


# login_manager = LoginManager()  # 创建LoginManager实例.
# login_manager.session_protection = 'strong'
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
# login_manager.login_message = 'Access denied.'
# login_manager.init_app(app)
# app.secret_key = 'random string'


def check_name(str):
    le = len(str)
    index = 0
    for ch in str:
        if u'\u4e00' <= ch <= u'\u9fff':
            index = index + 1
    if index == le:
        return True
    else:
        return False


class LoginForm(Form):
    username = TextField("username", [validators.Required()])
    password = PasswordField("password", [validators.Required()])


class InfoForm(Form):
    name = TextField("name", [validators.Required()])
    sign_time = TextField("sign_time", [validators.Required()])
    start_time = TextField("start_time", [validators.required()])
    end_time = TextField("end_time", [validators.Required()])
    simplify = TextField("simplify", [validators.Required()])


@app.route('/<identity>/<id>/raise_answer')
def raise_answer(id, identity):
    return render_template('raise_answer.html', id=id, identity=identity)


@app.route('/<identity>/<id>/self_center')
def self_center(id, identity):
    length = 0
    grade_list = 0
    if identity == '学生':
        lt = Student.query.filter_by(id=id).first()
        items = lt.com_infos
        length = len(items)
        grade_list = []
        for item in items:
            sql = " SELECT grade FROM table_stu_com WHERE com_id = '%s' and stu_id ='%s'" % (item.id, id)
            temp = db.session.execute(sql)
            for ll in temp:
                grade_list.append((ll[0]))
    elif identity == '老师':
        lt = Teacher.query.filter_by(id=id).first()
    elif identity == '赛事主办方':
        lt = Holder.query.filter_by(id=id).first()
    else:
        lt = Monitor.query.filter_by(id=id).first()
    db.session.close()
    return render_template("self_center.html", id=id, identity=identity, lt=lt, grade_list=grade_list, length=length)


@app.route('/<identity>/<id>/reset', methods=['GET', 'POST'])
def reset(id, identity):
    if request.method == 'POST':
        pass1 = request.values.get('password')
        pass2 = request.values.get('password1')
        if pass1 == pass2:
            com_infos = Com_info.query.all()
            notice_list = Notice.query.all()
            if identity == '学生':
                Student.query.filter_by(id=id).update({'password': pass1})
            elif identity == '老师':
                Teacher.query.filter_by(id=id).update({'password': pass1})
            elif identity == '赛事主办方':
                Holder.query.filter_by(id=id).update({'password': pass1})
            return redirect(url_for('home', id=id, identity=identity
                                    , com_infos=com_infos, notice_list=notice_list))
        else:
            flash('两次密码不一致')
            return render_template('reset.html', id=id, identity=identity)
    return render_template('reset.html', id=id, identity=identity)


@app.route('/<identity>/<id>/<name>/<status>/com_team')
def com_team(identity, id, name, status):
    com_info = Com_info.query.filter_by(name=name).first()
    sql = " SELECT grade FROM table_com_team WHERE com_id = '%s'" % com_info.id
    lst = db.session.execute(sql)
    lst_done = []
    teams = com_info.teams
    for ll in lst:
        lst_done.append(ll[0])
    teachers = com_info.teacher.split()
    judge = 0
    if identity == '老师':
        teacher_temp = Teacher.query.filter_by(id=id).first()
        if teacher_temp.name in teachers:
            judge = 1
            return render_template('com_team.html', com_info=com_info, teams=teams, id=id, identity=identity, name=name,
                                   judge=judge, len=len(com_info.students), status=status, lst_done=lst_done)
        else:
            return render_template('com_team.html', com_info=com_info, teams=teams, id=id, identity=identity, name=name,
                                   judge=judge, len=len(com_info.students), status=status, lst_done=lst_done)
    return render_template('com_team.html', com_info=com_info, teams=teams, id=id, identity=identity, name=name,
                           judge=judge, len=len(com_info.students), status=status, lst_done=lst_done)


@app.route('/<identity>/<id>/<name>/<status>/com_stus')
def com_stus(id, identity, name, status):
    com_new = Com_info.query.filter_by(name=name).first()
    sql = " SELECT grade FROM table_stu_com WHERE com_id = '%s'" % com_new.id
    lst = db.session.execute(sql)
    lst_done = []
    for ll in lst:
        print(ll[0])
        lst_done.append(ll[0])
    teachers = com_new.teacher.split()
    judge = 0
    if identity == '老师':
        teacher_temp = Teacher.query.filter_by(id=id).first()
        if teacher_temp.name in teachers:  # 判别是否是指导老师
            print('sc')
            judge = 1
            return render_template("com_stus.html", id=id, identity=identity, name=name, com_new=com_new, status=status,
                                   lst_done=lst_done, len=len(com_new.students), judge=judge)
        else:
            return render_template("com_stus.html", id=id, identity=identity, name=name, com_new=com_new, status=status,
                                   lst_done=lst_done, len=len(com_new.students), judge=judge)
    else:
        return render_template("com_stus.html", id=id, identity=identity, name=name, com_new=com_new, status=status,
                               lst_done=lst_done, len=len(com_new.students), judge=judge)


@app.route('/<identity>/<id>/<name>/<index>/stu_manage', methods=['GET', 'POST'])
def stu_manage(id, identity, name, index):
    com_temp = Com_info.query.filter_by(name=name).first()
    com_infos = Com_info.query.all()
    student_list = com_temp.students
    award_list = com_temp.award.split()
    assign_list = com_temp.assign.split()
    assign_list = list(map(int, assign_list))  # 字符串数组转换成int数组
    if request.method == 'POST':
        print(award_list)
        print(assign_list)
        grade1 = request.values.get("grade")
        for i in range(len(award_list)):
            if award_list[i] == grade1:
                print('--')
                assign_list[i] = assign_list[i] - 1
                # print(assign_list)
        ctr = str(assign_list[0])
        print(ctr)
        for i in range(1, len(award_list)):
            ctr = ctr + ' ' + str(assign_list[i])
        com_temp.assign = ctr
        db.session.commit()
        sql = "UPDATE table_stu_com SET grade = '%s' WHERE stu_id = '%s' AND com_id = '%s'" % (
            grade1, student_list[int(index)].id, com_temp.id)
        db.session.execute(sql)
        db.session.commit()
        index = int(index) + 1
        if index < len(student_list):
            return redirect(url_for('stu_manage', id=id, identity=identity, name=name, index=index))
        else:
            com_temp.status = 0
            db.session.commit()
            return render_template('com_list.html', id=id, identity=identity, com_infos=com_infos)
    length = len(award_list)
    db.session.close()
    return render_template('stu_manage.html', id=id, identity=identity, name=name, student_list=student_list,
                           index=int(index), award=award_list, length=length, assign_list=assign_list)


@app.route('/<identity>/<id>/<name>/<index>/team_manage', methods=['GET', 'POST'])
def team_manage(id, identity, name, index):
    com_temp = Com_info.query.filter_by(name=name).first()
    com_infos = Com_info.query.all()
    team_list = com_temp.teams
    print(team_list)
    award_list = com_temp.award.split()
    assign_list = com_temp.assign.split()
    assign_list = list(map(int, assign_list))  # 字符串数组转换成int数组
    if request.method == 'POST':
        grade1 = request.values.get("grade")
        for i in range(len(award_list)):
            if award_list[i] == grade1:
                assign_list[i] = assign_list[i] - 1
        ctr = str(assign_list[0])
        for i in range(1, len(award_list)):
            ctr = ctr + ' ' + str(assign_list[i])
        com_temp.assign = ctr
        db.session.commit()
        sql = "UPDATE table_com_team SET grade = '%s' WHERE team_id = '%s' AND com_id = '%s'" % (
            grade1, team_list[int(index)].id, com_temp.id)
        db.session.execute(sql)
        db.session.commit()
        index = int(index) + 1
        if index < len(team_list):
            return redirect(url_for('team_manage', id=id, identity=identity, name=name, index=index))
        else:
            com_temp.status = 0
            db.session.commit()
            return render_template('com_list.html', id=id, identity=identity, com_infos=com_infos)
    length = len(award_list)
    # print(team_list[int(index)].students)
    # let =3
    let = len(team_list[int(index)].students)
    db.session.close()
    return render_template('team_manage.html', id=id, identity=identity, name=name,
                           team_list=team_list, max_p=com_temp.max_p, let=let,
                           index=int(index), award=award_list
                           , length=length, assign_list=assign_list
                           )


@app.route('/<identity>/<id>/<name>/sc')
def signup_sc(id, identity, name):
    com_detail = Com_info.query.filter_by(name=name).first()
    return render_template('signup_sc.html', id=id, identity=identity, name=com_detail.name)


@app.route('/<identity>/<id>/<name>/detail', methods=['GET', 'POST'])
def detail(id, identity, name):
    com_detail = Com_info.query.filter_by(name=name).first()
    student1 = Student.query.filter_by(id=id).first()
    count = 0
    error = None
    if request.method == 'POST':
        # print('min:', com_detail.min_p)
        # print('max:', com_detail.max_p)
        for stu_comm in student1.com_infos:
            if stu_comm == com_detail:
                count = count + 1
        if count == 1:
            error = '你已经报名过了'
            return render_template('detail.html', id=id, identity=identity, com_detail=com_detail, error=error)
        else:
            if com_detail.min_p == com_detail.max_p == 1:
                student1.com_infos.append(com_detail)
                db.session.commit()
                return redirect(url_for('signup_sc', id=id, identity=identity, name=name))
            else:
                return redirect(url_for('esteam', id=id, identity=identity, name=name))
    db.session.close()
    return render_template('detail.html', id=id, identity=identity, com_detail=com_detail, error=error)


@app.route('/<identity>/<id>/<name>/esteam', methods=['GET', 'POST'])
def esteam(id, identity, name):
    student1 = Student.query.filter_by(id=id).first()
    if request.method == 'POST':
        global get_ajax_id
        get_ajax_id = request.values.get('ajax_item_id', 0)
        # print('get_ajax_id',get_ajax_id)
        if get_ajax_id != 0:
            ctr = json.loads(get_ajax_id)
            # print('ctr', ctr)
            com = Com_info.query.filter_by(name=name).first()
            team_new = Team()
            for i in range(len(ctr)):
                stu_name = ctr[i]['NAME']
                stu = Student.query.filter_by(name=stu_name).first()
                if stu in team_new.students:
                    flash(stu.name + '已存在')
                    return render_template('esteam.html', id=id, identity=identity, name=name, student=student1)
                else:
                    if stu in com.students:
                        flash(stu.name+'已报名该竞赛')
                        return render_template('esteam.html', id=id, identity=identity, name=name, student=student1)
                    else:
                        team_new.students.append(stu)
                        com.students.append(stu)
            com.teams.append(team_new)
            db.session.commit()
            return redirect(url_for('home', id=id, identity=identity))
        else:
            return redirect(url_for('home', id=id, identity=identity))
        # return render_template('esteam.html', id=id, identity=identity, name=name, student=student1)
    db.session.close()
    return render_template('esteam.html', id=id, identity=identity, name=name, student=student1)


@app.route('/<identity>/<id>/<name>/notice_detail')
def notice_detail(id, identity, name):
    notice_temp = Notice.query.filter_by(name=name).first()
    return render_template('notice_detail.html', id=id, identity=identity, notice=notice_temp)


@app.route('/home/put_cop/<identity>/<id>', methods=['GET', 'POST'])  # 发布竞赛信息
def put_cop(id, identity):
    # myform = InfoForm(request.form)
    charge = Holder.query.filter_by(id=id).first()
    hold = charge.name
    print(hold)
    if request.method == 'POST':
        name = request.values.get("name")
        # print(name)
        sign_time = request.values.get("sign_time")
        # print(sign_time)
        start_time = request.values.get("time")
        # print(start_time)
        end_time = request.values.get("end_time")
        # print(end_time)
        simplify = request.values.get("simplify")
        # print(simplify)
        com_level = request.values.get("com_level")
        com_place = request.values.get("com_place")
        org_party = request.values.get("org_party")
        teacher = request.values.get("teacher")
        award = request.values.get("award")
        assign = request.values.get("assign")
        pattern = request.values.get("pattern")
        put_time = datetime.date.today()
        f = request.files['file']
        fname = secure_filename(f.filename)
        if fname:
            ext = fname.rsplit('.', 1)[1]
            new_filename = str(name) + '.' + ext
            basepath = os.path.dirname(__file__)
            upload_path = os.path.join(basepath, 'static\\uploads', new_filename)
            f.save(upload_path)
        lt = Com_info.query.filter_by(name=name).first()
        if lt:
            print('competition exists')
            flash('已存在该竞赛')
            return render_template('put_cop.html', id=id, identity=identity)
        else:
            if pattern == '个人':
                min_p = 1
                max_p = 1
            else:
                result = re.findall(r"\d+", string=pattern)
                min_p = int(result[0])
                max_p = int(result[1])
            if varify_time(sign_time, start_time, end_time):
                com_info = Com_info(name=name, sign_time=sign_time, start_time=start_time, end_time=end_time,
                                    com_level=com_level, com_place=com_place, org_party=org_party,
                                    teacher=teacher, put_time=put_time, award=award, assign=assign, min_p=min_p,
                                    max_p=max_p, status=1, abstract=simplify, holder=hold, pattern=pattern)
                db.session.add(com_info)
                db.session.commit()
                return redirect(url_for('home', id=id, identity=identity))
            else:
                flash('时间安排不合理')
    db.session.close()
    return render_template('put_cop.html', id=id, identity=identity)


def varify_time(sign_time, start_time, end_time):  # 验证时间是否有效
    date = datetime.date.today()
    today = datetime.datetime.strptime(str(date), '%Y-%m-%d')
    sign_time = datetime.datetime.strptime(sign_time, '%Y-%m-%d')
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
    print(today, sign_time, start_time, end_time)
    if today < sign_time < start_time < end_time:
        return True
    else:
        return False


@app.route('/<identity>/<id>/sign_up/<com_info>')
def sign_up(identity, id, com_info):
    return render_template('signup.html', identity=identity, id=id, com_info=com_info)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id = request.values.get("id")
        name = request.values.get("name")
        age = request.values.get("age")
        dept = request.values.get("dept")
        password1 = request.values.get("inputPassword")
        password2 = request.values.get("confirmPassword")
        print(id, name, age, dept, password1)
        if password1 == password2:
            if Student.query.filter_by(id=id).first():
                flash('用户已存在')
                return render_template('register.html')
            else:
                if check_name(name):
                    student_t = Student(id=id, name=name,
                                        age=age, dept=dept,
                                        password=password1)
                    db.session.add(student_t)
                    db.session.commit()
                    return redirect(url_for('hello_world'))
                else:
                    flash('请输入中文姓名')
                    return render_template('register.html')
        else:
            flash('请确保两次密码一致')
            return render_template('register.html')
    db.session.close()
    return render_template('register.html')


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/', methods={'POST', 'GET'})  # 登录页面
def hello_world():
    myForm = LoginForm(request.form)
    if request.method == 'POST':
        identity = request.values.get("manufacturer")
        id = request.values.get("id")
        password = request.values.get("password")
        if identity == '学生':
            lt = Student.query.filter_by(id=id, password=password).first()
        elif identity == '老师':
            lt = Teacher.query.filter_by(id=id, password=password).first()
        elif identity == '赛事主办方':
            lt = Holder.query.filter_by(id=id, password=password).first()
        else:
            lt = Monitor.query.filter_by(id=id, password=password).first()
        if lt:
            user = Admin.query.filter_by(id='zwk', password='123456')
            # login_user(user)
            return redirect(url_for('home', identity=identity, id=id))
        else:
            message = "Login failed"
            return render_template('login.html', message=message, form=myForm)
    return render_template('login.html', form=myForm)


@app.route('/home/<identity>/<id>', methods=['GET', 'POST'])  # 主页
# @login_required
def home(id, identity):
    com_infos = Com_info.query.all()
    notice_list = Notice.query.all()
    g.com_list = com_infos
    # print(g.com_list)
    return render_template('main.html', id=id, identity=identity,
                           com_infos=com_infos, notice_list=notice_list)


@app.route('/<identity>/<id>/com_list')
def com_list(id, identity):
    com_infos = Com_info.query.all()
    return render_template('com_list.html', id=id, identity=identity, com_infos=com_infos
                           # , paginate=paginate
                           )


@app.route('/<identity>/<id>/notice_list')
def notice_list(id, identity):
    notice_lists = Notice.query.all()
    return render_template('notice_list.html', id=id, identity=identity, notice_lists=notice_lists)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500


if __name__ == '__main__':
    print('hello,app.py')
    app.run()
