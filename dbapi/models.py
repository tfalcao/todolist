__author__ = 'cody'

from sqlalchemy.ext.declarative import declarative_base as real_declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from dbapi import app_bcrypt
from bcrypt import gensalt
from datetime import datetime


# The below code was taken from
# https://blogs.gnome.org/danni/2013/03/07/generating-json-from-sqlalchemy-objects/
# with an added fromdict() method

# Let's make this a class decorator
declarative_base = lambda cls: real_declarative_base(cls=cls)

@declarative_base
class Base(object):
    """
    Add some default properties and methods to the SQLAlchemy declarative base.
    """

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def todict(self):
        return self.columnitems

    def fromdict(self, dict_obj):
        forbidden_fields = ["id", "required_fields"]
        [dict_obj.__delitem__(field) for field in forbidden_fields if field in dict_obj]
        [self.__setattr__(key, dict_obj[key]) for key in dict_obj.keys() if key in self.columns]

# Define our schema

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    salt = Column(String(50))
    tasks = relationship("Task", cascade="all, delete-orphan", back_populates="user")
    required_fields = ["username", "password"]

    def __init__(self, dict_obj=None):
        if dict_obj is None:
            dict_obj = {}
        self.fromdict(dict_obj)

    def set_password(self, password):
        self.salt = gensalt()
        self.password = app_bcrypt.generate_password_hash(self.salt + str(password))

    def check_password(self, password):
        return app_bcrypt.check_password_hash(self.password, self.salt + str(password))

    def todict(self, recurse=True):
        data = super().todict()
        # We don't want to reveal the salt or password
        if "password" in data:
            del data["password"]
        if "salt" in data:
            del data["salt"]
        if recurse:
            if hasattr(self, "tasks") and self.tasks is not None:
                data["tasks"] = [task.todict(recurse=False) for task in self.tasks]
            else:
                data["tasks"] = []
        return data

    def fromdict(self, dict_obj):
        super().fromdict(dict_obj)
        # We want to make sure that the password is stored in the database as a hash
        if "password" in dict_obj:
            self.set_password(dict_obj["password"])


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    points = Column(Integer, default=0)
    start = Column(DateTime)
    end = Column(DateTime)
    desc = Column(String(1000))
    userid = Column(Integer, ForeignKey("user.id"))
    required_fields = ["name"]

    user = relationship("User", back_populates="tasks")

    def __init__(self, dict_obj=None):
        if dict_obj is None:
            dict_obj = {}
        self.fromdict(dict_obj)

    def todict(self, recurse=True):
        data = super().todict()
        if recurse:
            if hasattr(self, "user") and self.user is not None:
                data["user"] = self.user.todict(recurse=False)
            else:
                data["user"] = None
        return data

    def fromdict(self, dict_obj):
        super().fromdict(dict_obj)
        if "start" in dict_obj and dict_obj["start"] is not None:
            self.start = datetime.utcfromtimestamp(dict_obj["start"])
        if "end" in dict_obj and dict_obj["end"] is not None:
            self.end = datetime.utcfromtimestamp(dict_obj["end"])



