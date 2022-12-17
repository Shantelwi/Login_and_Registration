from flask_app import app
from flask import render_template, request, redirect, session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask_app.models.post import Post

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/register/user', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['id'] = id

    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user = User.get_by_email(data)
    # user is not registered in the db
    if not user:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['id'] = user.id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': session['id']
    }
    return render_template("dashboard.html", user = User.get_by_id(data),all_posts = Post.get_all_posts_with_user())

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

