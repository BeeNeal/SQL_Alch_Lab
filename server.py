"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """show list of users."""

    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/register', methods=['GET'])
def register_form():
    """render the registration form."""
    return render_template("registration.html")

@app.route('/register', methods=['POST'])
def register_process():
    """Collect user information, submit to DB"""

    email = request.form.get('email')
    password = request.form.get('password')

    all_users = db.session.query(User.email).all() #list of all user emails from User table
    print all_users

    if email not in all_users:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        print "User added!"
    else:
        print "User has already been added!"

    return redirect("/")

@app.route('/login', methods=['GET'])
def display_login():
    """display login page"""
    if 'user' in session: # ask about sessions
        return redirect("/")
    else:
        return render_template('login.html')

@app.route('/login', methods=["POST"])
def login():
    """Check that email and password match user email and password in DB"""

    email = request.form.get('email')
    password = request.form.get('password')

    # expecting user object for below query
    # user = db.session.query(User).filter_by(email = email).first() #why does this not work?
    user = User.query.filter(User.email == email).first()

    print "THIS IS IT!!!!!!!!!*******{}".format(user) 

    if not user:  # == None
        flash("Please register")
        return redirect('/register')

    if password == user.password:
        session['user'] = email  # check this
        flash("successfully logged in!")

        return redirect('/')
    else:
        flash("Incorrect password! Try again")
        return redirect('/login')


@app.route('/logout')
def logout():
    """logs user out - deletes user from session"""

    if 'user' in session:
        del session['user']
    else:
        flash("You are not logged in!")

    return redirect('/login')

@app.route('/users/<user.user_id>') 
def userinfo():
    """Page that shows info about a particular user"""
    flash("User info yay!")

    user = User.query.filter(User.user_id == user.user_id).first()


    return render_template('indiv_user.html') #pass user object to jinja; unpack in jinja


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
