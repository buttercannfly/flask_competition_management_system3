from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user, login_required
from wtforms import Form, TextField, PasswordField, validators
import hello
import datetime
from hello import *

hello  # 调用hello初始化模板
app = Flask(__name__)
# app.secret_key = ''
bootstrap = Bootstrap(app)
app.debug = True
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'random string'


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
def raise_answer(id,identity):
    return render_template('raise_answer.html', id=id, identity=identity)


@app.route('/<identity>/<id>/self_center')
def self_center(id,identity):
    if identity == '学生':
        lt = Student.query.filter_by(id=id).first()
    elif identity == '老师':
        lt = Teacher.query.filter_by(id=id).first()
    elif identity == '赛事主办方':
        lt = Holder.query.filter_by(id=id).first()
    else:
        lt = Monitor.query.filter_by(id=id).first()
    return render_template("self_center.html", id=id, identity=identity, lt=lt)


@app.route('/<identity>/<id>/<name>/<status>/com_stus')
def com_stus(id,identity,name,status):
    com_new = Com_info.query.filter_by(name=name).first()
    print(status)
    print(identity)
    return render_template("com_stus.html", id=id, identity=identity,name=name, com_new=com_new,status=status)


@app.route('/<identity>/<id>/<name>/stu_manage',methods=['GET','POST'])
def stu_manage(id,identity,name):
    com_temp = Com_info.query.filter_by(name=name).first()
    student_list = com_temp.students
    if request.method == 'POST':
        grade = request.values.get("grade")
        print(grade)

    return render_template('stu_manage.html', id=id, identity=identity, name=name,student_list=student_list)


@app.route('/<identity>/<id>/<name>/sc')
def signup_sc(id,identity,name):
    com_detail = Com_info.query.filter_by(name=name).first()
    return render_template('signup_sc.html', id=id, identity=identity, name=com_detail.name)


@app.route('/<identity>/<id>/<name>/detail', methods=['GET', 'POST'])
def detail(id,identity,name):
    com_detail = Com_info.query.filter_by(name=name).first()
    student1 = Student.query.filter_by(id=id).first()
    count = 0
    print(com_detail.status)
    error = None
    if request.method == 'POST':
        for stu_comm in student1.com_infos:
            if stu_comm == com_detail:
                count = count + 1
        if count == 1:
            error='你已经报名过了'
            return render_template('detail.html', id=id, identity=identity, com_detail=com_detail,error=error)
        else:
            error=None
            student1.com_infos.append(com_detail)
            db.session.commit()
            return redirect(url_for('signup_sc',id=id,identity=identity,name=name))
    return render_template('detail.html', id=id, identity=identity, com_detail=com_detail,error=error)


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
        lt = Com_info.query.filter_by(name=name, sign_time=sign_time, start_time=start_time, end_time=end_time,
                                      abstract=simplify).first()
        if lt:
            print('competition exists')
            return render_template('put_cop.html', id=id, identity=identity)
        else:
            com_info = Com_info(name=name, sign_time=sign_time, start_time=start_time, end_time=end_time,
                                abstract=simplify, holder=hold)
            db.session.add(com_info)
            db.session.commit()
            return redirect(url_for('home', id=id, identity=identity))
    return render_template('put_cop.html', id=id, identity=identity)


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
        print(id,name,age,dept,password1)
        if password1 == password2:
            if Student.query.filter_by(id=id).first():
                    return render_template('register.html')
            else:
                    student_t = Student(id=id, name=name,
                                    age=age, dept=dept,
                                    password=password1)
                    db.session.add(student_t)
                    db.session.commit()
                    return redirect(url_for('hello_world'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/', methods={'POST', 'GET'})  # 登录页面
def hello_world():
    myForm = LoginForm(request.form)
    if request.method == 'POST':
        identity = request.values.get("manufacturer")
        print(identity)
        id = request.values.get("id")
        print(id)
        password = request.values.get("password")
        if identity == '学生':
            lt = Student.query.filter_by(id=id, password=password).first()
        elif identity == '老师':
            lt = Teacher.query.filter_by(id=id,password=password).first()
        elif identity == '赛事主办方':
            lt = Holder.query.filter_by(id=id, password=password).first()
        else:
            lt = Monitor.query.filter_by(id=id, password=password).first()
        if lt:
            return redirect(url_for('home', identity=identity, id=id))
        else:
            message = "Login failed"
            return render_template('login.html', message=message, form=myForm)
    return render_template('login.html', form=myForm)


@app.route('/home/<identity>/<id>',methods=['GET','POST'])  # 主页
def home(id, identity):
    com_infos = Com_info.query.all()
    today = datetime.date.today()
    for com_info in com_infos:
        if com_info.sign_time >= today:
            com_info.status = 1
            db.session.commit()
        elif com_info.start_time <= today <= com_info.end_time:
            com_info.status = 2
            db.session.commit()
        elif com_info.end_time<=today:
            com_info.status =0
            db.session.commit()
    return render_template('main.html', id=id, identity=identity, com_infos=com_infos)


@app.route('/<identity>/<id>/com_list')
def com_list(id,identity):
    com_infos = Com_info.query.all()
    return render_template('com_list.html',id=id,identity=identity,com_infos=com_infos)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500


if __name__ == '__main__':
    print('hello,app.py')
    app.run()
