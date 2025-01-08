from flask import Flask, render_template, redirect, url_for, flash, session
from extensions import db

from models import User
from forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd123e4f5g678h901i2j3k4l5m6n7o8p9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    check = check_access(True)
    if check:
        return check
    return "It works!"

@app.route('/register', methods=['GET','POST'])
def register():
    check = check_access(False)
    if check:
        return check

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have registered!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    check = check_access(False)
    if check:
        return check

    form = LoginForm()
    if form.validate_on_submit():
        # User search
        user = User.query.filter_by(name=form.username.data).first()
        if user and check_password_hash(user.hash_pass, form.password.data):
            # Create a session
            session['user_id'] = user.id
            flash('You have successfully logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    check = check_access(True)
    if check:
        return check

    session.pop('user_id', None)
    flash('You have successfully logged out', 'success')
    return redirect(url_for('login'))

def check_access(expected):
    if expected and 'user_id' not in session:
        flash('Please log in', 'warning')
        return redirect(url_for('login'))
    elif not expected and 'user_id' in session:
        flash('You have already logged in', 'warning')
        return redirect(url_for('index'))
    return None

if __name__ == "__main__":
    app.run(debug=True)