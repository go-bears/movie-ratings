"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Ratings, Movie, connect_to_db, db

from datetime import datetime


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""


    return render_template("homepage.html", logged_in=session.get('email', False))


@app.route('/login_completion', methods=["POST"])
def login_completion():
    """Login resolution page, takes in login info, checks db for login or adds user"""

    email = request.form.get('username')
    password =request.form.get('password')

    print email, password

    # successful login    
    if db.session.query(User).filter((User.email==email) & (User.password==password)).first():
        print "Database queried!"
        flash("You are now logged in!")
        session['email'] = email
        return render_template("homepage.html", logged_in=session.get('email', False))

    # email already exists -- incorrect password
    elif db.session.query(User).filter(User.email==email).first():
        flash("The password does not match the user email. Try Again!")
        return render_template('login_form.html', logged_in=session.get('email', False)) 

    # no email in db -- new user add
    elif not db.session.query(User).filter((User.email==email) & (User.password==password)).first():
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['email'] = email
        flash("Hi! We added you the database")

        print "I commited ", new_user, "to the database"
        return render_template("homepage.html", logged_in=session.get('email', False))
    

@app.route("/log_out")
def logging_out():
    """Logs User out of Ratings & clears Flask session dictionary """
    
    session.pop('email', None)
    flash("Thanks! You are now logged out")

    return render_template("homepage.html", logged_in=session.get('email', False))


@app.route("/login")
def login_form():
    """Displays user login form."""

    
    return render_template("login_form.html", logged_in=session.get('email', False))


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users, logged_in=session.get('email', False))


@app.route("/users/<int:user_id>")
def user_page(user_id):
    """Displays User profile information and movies they've rated"""

    # fetch the user based on their ID
    user = db.session.query(User).get(user_id)

    # unpack info from the user instance by checking attributes
    zipcode = user.zipcode
    age = user.age

    #list of ratings for the user. navigating attributes from user to ratings
    ratings_list = user.ratings

    # render these things to user_page.html: zipcode and age
    # (2) pass ratings associated with user_id  and pass list to jinga template on 
    # user_page.html. And have jinga unpack the  movie title

    return render_template("user_page.html", zipcode=zipcode,
                                             age=age,
                                             ratings_list=ratings_list,
                                             logged_in=session.get('email', False))

# make a page to list all movie :pass list

# set a route to all_movies_pages

# query db to get all movies
@app.route("/movies")
def movies_list():
    """Show list of movies."""

    movies = Movie.query.order_by(Movie.title).all()
    return render_template("movie_list.html", movies=movies, logged_in=session.get('email', False))


# make  details page for each movie; page displays all ratings, imdb url

# check Flask session to check if user is logged in:
#   if yes: able to set a rating or update current rating
 
@app.route("/movies/<int:movie_id>")
def movie_detail(movie_id):
    """Displays Movie detail information; logged_in user can rate or update movie ratings"""

    # fetch the movie details by movie_ID
    movie = db.session.query(Movie).get(movie_id)

    title = movie.title
    release_date = movie.release_date.strftime('%B %d, %Y')
    imdb_url = movie.imdb_url
    ratings_list = movie.ratings

    total = sum(r.score for r in ratings_list)

    avg_rating = float(total / len(ratings_list))

    user = db.session.query(User).filter(User.email==session['email']).one()

    user_rating = None

    for r in user.ratings:
        if r.movie_id == movie_id:
            user_rating = r.score

    return render_template("movie_page.html", title=title,
                                              release_date=release_date,
                                              imdb_url=imdb_url,
                                              avg_rating=avg_rating,
                                              user_rating = user_rating,
                                              ratings_list=ratings_list,
                                              movie_id = movie_id,
                                              logged_in=session.get('email', False))


@app.route("/new_rating/<int:movie_id>")
def update_rating(movie_id):
    pass



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
