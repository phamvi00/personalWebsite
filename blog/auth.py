from flask import(
    Blueprint, render_template, request, redirect, url_for, flash, session, g
)
from .db import get_db
from functools import wraps

bp = Blueprint("auth", __name__)

@bp.before_app_request
def load_user():
    id = session.get('id')
    if not id:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute('SELECT * FROM users WHERE id = {}'.format(id)).fetchone()

#this function is to check if the user is logged in and to protect
#some function from the public eye
def require_login(f):
    @wraps(f)
    #*: if you dont know how many parameters. **: the parameters has to be named
    def decorated_function(*args, **kws):
        if not g.user:
            return redirect(url_for('blog.main_page'))
        return f(*args, **kws)
    return decorated_function


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM users WHERE username='{}'".format(username)).fetchone()

        if not username:
            error = "You need to enter username."
        elif not password:
            error = "You need to enter password."
        elif user is None:
            error = "This username {} doesn't exist".format(username)
        elif password != user["password"]:
            error = "Wrong password!"
        else:
            session.clear()
            session['id'] = user["id"]
            return redirect(url_for('blog.main_page'))

        flash(error)

    return render_template('auth/login.html')


@bp.route("/register", methods=("GET","POST"))
def register():
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()    #return the database
        error = None
        user = db.execute("SELECT * FROM users WHERE username = '{}'".format(username)).fetchone()

        if not username:
            error = "You need to enter username."
        elif not password:
            error = "You need to enter password."
        elif user is not None:
            error = "This username {} already exists".format(username)
        else:
            db.execute("INSERT INTO users (username, password) VALUES ('{}','{}')".format(username, password))
            db.commit()
            #commit to end the current transaction and make permanent changes

            return redirect(url_for('auth.login'))
            #take the module auth and function login

        flash(error)
    return render_template('auth/register.html')
    #Flask finds a template file,
    #read the template, fuel data, and render to the user


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.main_page'))
