from flask import Flask, render_template, redirect, url_for, flash, session, request
from extensions import db

from models import User, Task
from forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash

from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd123e4f5g678h901i2j3k4l5m6n7o8p9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Main route
@app.route('/')
def index():
    check = check_access(True)
    if check:
        return check
    
    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', tasks=tasks)

# Users routes
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

# Tasks routes
@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    check = check_access(True)
    if check:
        return check
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = request.form.get('due_date')
      
        #Converting date from the form
        due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None

        new_task = Task(
            title = title,
            description=description,
            due_date=due_date,
            user_id=session['user_id']
        )
    
        db.session.add(new_task)
        db.session.commit()
        flash('Task created', 'success')
        return redirect(url_for('index'))
    return render_template('create_task.html')

@app.route('/tasks/delete/<int:id>', methods=['GET', 'POST'])
def delete_task(id):
    check = check_access(True)
    if check:
        return check
    
    #Checking id existence
    task = Task.query.get(id)
    if not task:
        flash('Task not found', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted', 'success')
        return redirect(url_for('index'))
    return render_template('delete_task.html', task=task)

@app.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    check = check_access(True)
    if check:
        return check
    
    #Checking id existence
    task = Task.query.get(id)
    if not task:
        flash('Task not found', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            title = task.title
            
        description = request.form.get('description')
        if not description:
            description = task.description
            
        due_date = request.form.get('due_date')
        if due_date:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        else:
            due_date = task.due_date
        
        #Updating
        task.title = title
        task.description = description
        task.due_date = due_date
        db.session.commit()
        flash('Task updated', 'success')
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

# Access checker
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