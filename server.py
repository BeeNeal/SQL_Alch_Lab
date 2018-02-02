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
    user_ratings = Rating.query.filter(Rating.user_id == user_id).all() #why .all not needed
    #user_ratings = db.session.query(Rating).filter_by(user_id=user_id).all()
    print user_ratings

    return render_template('indiv_user.html',user=user, user_ratings=user_ratings) #pass user object to jinja; unpack in jinja


@app.route('/movies')
def showmovie():
    """Show page of list of movies"""

    movies = db.session.query(Movie).order_by(Movie.title).all()

    return render_template('movies.html',movies=movies)

@app.route('/movies/<movie_title>')
def movieInfo(movie_title):
    """Display info about movie"""

    movie = Movie.query.filter_by(title=movie_title).first()
    # movie_ratings = db.session.query(Rating).filter_by(Movie.title=movie_title).all()
    # movie_ratings = db.session.query(Rating).filter(movie.title == movie_title).all()

    # r = movie.query.filter(movie.title == movie_title)

    # movie_ratings = db.session.query(Rating).filter(Rating.movie_id == 10).all()

    # movie_object = db.session.query(Movie).filter_by(title=movie_title).first()

    # movie_ratings = db.session.query(Rating).filter(Rating.movies.movie_object == movie_title).all()

    # all_ratings_4 = Rating.query.filter_by(score=4).all()
    # all movies that user 200 has rated

    # Rating.query.filter_by(user_id=200).all() - practice

    # #User table; using user ID 200; get back user object

    # user200 = User.query.filter_by(user_id=200).first() #gets user object - practice
    # user200.ratings - practice


    return render_template('indiv_movie.html', movie=movie)

@app.route('/movies/addrating' methods=["POST"])
def addRating():
    """Processing movie rating form"""
    # do a lookup query to get user ID from user email. save the user ID
    # get list of all movies rated from user_id (as a movie object) -- or from user email
    # query the list of movies to see if user has rated that movie



    new_rating = request.form.get('rating')

    #user_id = User.query.filter_by(email=[user email])

    #user_rated_movies = Ratings.query.filter_by(user_id = user_id) #or we can get user_id
    #user_rated_movies.filter_by(movie.title)



    #is User logged in?
    if 'user' in session:
        user_email = session['user']
        if 
        #check DB
            return redirect("/")
        else:
            flash('Please login to rate!')
            return redirect('login.html')




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
