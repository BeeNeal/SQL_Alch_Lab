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

@app.route('/users/<int:user_id>')
def userinfo(user_id):   # argument can be passed to view function from URL this way
    """Page that shows info about a particular user"""
    flash("User info yay!")

    user = User.query.filter(User.user_id == user_id).first()
    # print user
    user_ratings = db.session.query(Rating).filter(Rating.user_id == user_id).all() #why .all not needed
    #user_ratings = db.session.query(Rating).filter_by(user_id=user_id).all()
    print user_ratings

    return render_template('indiv_user.html',user=user, user_ratings=user_ratings) #pass user object to jinja; unpack in jinja


@app.route('/movies')
def showmovie():
    """Show page of list of movies"""

    movies = db.session.query(Movie).order_by(Movie.title).all()
    print "THIS ************!!!!!!!!!!!!!^^^^^^^^^^^^"
    print movies

    return render_template('movies.html',movies=movies)

@app.route('/movies/<movie_title>')
def movieInfo(movie_title):
    """Display info about movie"""

    movie = db.session.query(Movie).filter_by(title=movie_title).first()
    # movie_ratings = db.session.query(Rating).filter_by(Movie.title=movie_title).all()
    movie_ratings = db.session.query(Rating).filter(movie.title == movie_title).all()

    r = movie.query.filter(movie.title == movie_title)
    return render_template('indiv_movie.html', movie=movie, movie_ratings=movie_ratings)

#     SELECT movies.movie_id AS movies_movie_id, movies.title AS movies_title, movies.released_at AS movies_released_at, movies.imdb_url AS movies_imdb_url 
# FROM movies, users 
# WHERE users.user_id = %(user_id_1)s

    #not quite working - movie titles aren't lining up with correct user_id

    # trying to find all movies rated from user_id
    # SQL: SELECT title FROM movies JOIN ratings USING (movie_id) 
    # JOIN users ON (users.user_id = ratings.user_id) WHERE users.user_id = 942;
    #translate to SQLAlch




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
