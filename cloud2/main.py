from flask import Flask, render_template, redirect
from flask_login import LoginManager
from data import db_session
from data import users, jobs
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
import datetime

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class RegisterForm(FlaskForm):
    login = StringField("Login / email", validators=[DataRequired()])
    password = PasswordField("Password")
    password_again = PasswordField("Repeat password")
    surname = StringField("Surname", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    position = StringField("Position", validators=[DataRequired()])
    speciality = StringField("Speciality", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField("Submit")


def main():
    db_session.global_init("db/mars.sqlite")
    app.run()


@app.route("/")
def log():
    session = db_session.create_session()
    jobbs = session.query(jobs.Jobs)
    team_leader = []
    for i in jobbs:
        leader = int(i.team_leader)
        team_leader += [session.query(users.User).filter(users.User.id == leader).first()]
    return render_template("log.html", jobs=jobbs, team_leader=team_leader)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.password_again.data:
            session = db_session.create_session()
            user = users.User()
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.position = form.position.data
            user.speciality = form.speciality.data
            user.address = form.address.data
            user.email = form.login.data
            for i in session.query(users.User):
                if i.email == user.email:
                    return "Пользователь с таким логином уже есть"
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect("/")
        else:
            return "Пароли не совпадают"
    return render_template("register.html", title="Регистрация", form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


if __name__ == '__main__':
    main()