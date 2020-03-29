"""Utility file to seed zoomers database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Schedule
from model import Type
from model import Activity, ActivityType, ScheduleActivity

from datetime import datetime
from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print("Users")

    User.query.delete()

    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, username, email, password, zipcode = row.split("|")

        user = User(user_id=user_id,
                    username=username,
                    email=email,
                    zipcode=zipcode)

        user.set_password(password)

        db.session.add(user)

    db.session.commit()


def load_schedules():
    """Load schedules into database."""

    print("Schedules")

    Schedule.query.delete()

    for row in open("seed_data/u.schedule"):
        row = row.rstrip().split("|")

        schedule_id = row[0]
        title = row[1]

        schedule = Schedule(schedule_id=schedule_id,
                      title=title)

        db.session.add(schedule)

    db.session.commit()


def load_types():
    """Load types into database."""

    print("Types")

    Type.query.delete()

    for row in open("seed_data/u.type"):
        row = row.rstrip()
        type_id, type = row.split("|")

        type = Type(type_id=type_id,
                        type=type)

        db.session.add(type)

    db.session.commit()

def load_activities():
    """Load activities into database."""

    print("Activities")

    Activity.query.delete()

    for row in open("seed_data/u.activity"):
        row = row.rstrip().split("|")

        activity_id = row[0]
        title = row[1]

        if len(row)>2:
            link = row[2]
        else:
            link = None
            
        activity = Activity(activity_id=activity_id, title=title, link=link)

        db.session.add(activity)

    db.session.commit()

# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""
#
#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])
#
#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()
#
# def set_val_schedule_id():
#     """Set value for the next schedule_id after seeding database"""
#
#     result = db.session.query(func.max(Schedule.schedule_id)).one()
#     max_id = int(result[0])
#
#     query = "SELECT setval('schedules_schedule_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()
#
# def set_val_type_id():
#     """Set value for the next type_id after seeding database"""
#
#     result = db.session.query(func.max(Type.type_id)).one()
#     max_id = int(result[0])
#
#     query = "SELECT setval('types_type_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_schedules()
    load_types()
    load_activities()

    # set_val_user_id()
    # set_val_schedule_id()
    # set_val_type_id()
