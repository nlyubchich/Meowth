from flask import render_template, Blueprint, flash, session, redirect, url_for
from .forms import LoginForm, RegisterForm
from .decorators import login_required
from project.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.bl.authenticate(**form.data)
        if user:
            session['user_id'] = user.id
            return redirect(url_for('admin.vacancy_list'))
        else:
            flash("Неправильный логин и/или пароль")

    if session.get('user_id'):
        return redirect(url_for('admin.vacancy_list'))

    return render_template(
        'login.html',
        title='Sign in',
        form=form,
    )


@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        userdata = form.data
        userdata.pop('confirmation')
        User.bl.create_user(userdata)
        flash("Вы успешно зарегистрировались")
        return redirect(url_for('auth.login'))

    return render_template(
        'login.html',
        title='Registration',
        form=form,
    )


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))
