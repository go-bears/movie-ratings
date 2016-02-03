"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Ratings, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/login_completion', methods=["POST"])
def login_completion():
    """Homepage."""

    email = request.form.get('username')
    password =request.form.get('password')

    print email, password

    # successful login    
    if db.session.query(User).filter((User.email==email) & (User.password==password)).first():
        print "Database queried!"
        flash("You are now logged in!")
        session['email'] = email
        return render_template("homepage.html")

    # email already exists -- incorrect password
    elif db.session.query(User).filter(User.email==email).first():
        flash("The password does not match the user email. Try Again!")
        return render_template('login_form.html') 

    # no email in db -- new user add
    elif not db.session.query(User).filter((User.email==email) & (User.password==password)).first():
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['email'] = email
        flash("Hi! We added you the database")

        print "I commited ", new_user, "to the database"
        return render_template("homepage.html")
    

@app.route("/log_out")
def logging_out():
    """Logs User out of Ratings & clears Flask session dictionary """
    
    session.pop('email', None)
    flash("Thanks! You are now logged out")
        
    return render_template("homepage.html")


@app.route("/login")
def login_form():
    """Displays user login form."""

    
    return render_template("login_form.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
