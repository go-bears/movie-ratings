"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide a better display for object info when printed"""

        return "<User user_id=%s email=%s>" %(self.user_id, self.email)


# Put your Movie and Rating model classes here.
class Movie(db.Model):
    """ Movie Information Object """

    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    imdb_url = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        """Provide a better display for object info when printed"""

        return "<Movie movie_id=%s title=%s>" %(self.movie_id, self.title)

class Ratings(db.Model):
    """docstring for Ratings"""
    
    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    # set foreign keys from user and movie tables
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)

    # set relationship between Ratings and User & Movie classes
    movies = db.relationship('Movie')
    users = db.relationship('User')

    def __repr__(self):
        """Provide a better display for object info when printed"""

        return "<Ratings rating_id=%s score=%s user_id=%s movie_id=%s>" \
        %(self.rating_id, self.score, self.user_id, self.movie_id)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
