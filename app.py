from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user, login_required
from wtforms import Form, TextField, PasswordField, validators
import hello
from hello import *

hello  # 调用hello初始化模板
app = Flask(__name__)
# app.secret_key = ''
bootstrap = Bootstrap(app)
app.debug = True
login_manager = LoginManager()
login_manager.init_app(app)



class LoginForm(Form):
    username = TextField("username", [validators.Required()])
    password = PasswordField("password", [validators.Required()])


class InfoForm(Form):
    name = TextField("name", [validators.Required()])
    sign_time = TextField("sign_time", [validators.Required()])
    start_time = TextField("start_time", [validators.required()])
    end_time = TextField("end_time", [validators.Required()])
    simplify = TextField("simplify", [validators.Required()])


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
            com_info = Com_info(name=name, sign_time=sign_time, start_time=start_time,end_time=end_time,abstract=simplify, holder=hold)
            db.session.add(com_info)
            db.session.commit()
            return redirect(url_for('home', id=id, identity=identity))
    return render_template('put_cop.html', id=id, identity=identity)


@app.route('/sign_up')
def sign_up():
    return render_template('signup.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/', methods={'POST', 'GET'})  # 登录页面
def hello_world():
    myForm = LoginForm(request.form)
    if request.method == 'POST':
        identity = request.values.get("manufacturer")
        id = myForm.username.data
        password = myForm.password.data
        if identity == '学生':
            lt = Student.query.filter_by(id=id, password=password).first()
        elif identity == '老师':
            pass
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


@app.route('/home/<identity>/<id>')  # 主页
def home(id, identity):
    com_infos = Com_info.query.all()
    print(com_infos)
    return render_template('main.html', id=id, identity=identity, com_infos=com_infos)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500


if __name__ == '__main__':
    print('hello,app.py')
    app.run()
