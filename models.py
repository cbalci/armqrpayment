#!/usr/bin/pyton

import datetime
from google.appengine.ext import db

class Payment(db.Model):
    amount = db.StringProperty()
    company = db.StringProperty()
    complete = db.BooleanProperty()
    token = db.StringProperty()
