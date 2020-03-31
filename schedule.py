import requests
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from model import connect_to_db, db
from model import User, Schedule, Type
from model import Activity, ActivityType, ScheduleActivity

import server
# from server import app
