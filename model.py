"""Models and database functions."""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Baby-Zoomers website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password_hash = db.Column(db.String(128), nullable=False)
    zipcode = db.Column(db.String(15))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"


class Schedule(db.Model):
    """Schedule Data."""

    __tablename__ = "schedules"

    schedule_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(120), nullable=False)

    activities = db.relationship("Activity",
                             secondary="schedule_activities",
                             backref="schedules")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Schedule schedule_id={self.schedule_id} schedule_title={self.title}>"


class Type(db.Model):
    """Type of activity data."""

    __tablename__ = 'types'

    type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type = db.Column(db.String(50), unique=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Type type_id={self.type_id} type={self.type}>"


class Activity(db.Model):
    """Activity data."""

    __tablename__ = 'activities'

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50))

    types = db.relationship("Type",
                             secondary="activity_types",
                             backref="activities")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Activity_id={self.activity_id} title={self.title}>"


class ActivityType(db.Model):
    """Activity type of a specific activity."""

    __tablename__ = 'activity_types'

    activity_type_id = db.Column(db.Integer, primary_key=True)

    activity_id = db.Column(db.Integer,
                        db.ForeignKey('activities.activity_id'),
                        nullable=False)

    type_id = db.Column(db.Integer,
                         db.ForeignKey('types.type_id'),
                         nullable=False)

class ScheduleActivity(db.Model):
    """Activities of a specific schedule."""

    __tablename__ = 'schedule_activities'

    schedule_activity_id = db.Column(db.Integer, primary_key=True)

    activity_id = db.Column(db.Integer,
                        db.ForeignKey('activities.activity_id'),
                        nullable=False)

    schedule_id = db.Column(db.Integer,
                         db.ForeignKey('schedules.schedule_id'),
                         nullable=False)


######################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///zoomers'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
