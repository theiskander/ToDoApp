from flask import Flask, render_template, redirect, url_for, flash
from extensions import db

from models import User
from forms import RegistrationForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd123e4f5g678h901i2j3k4l5m6n7o8p9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return "It works!"

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have registered!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)