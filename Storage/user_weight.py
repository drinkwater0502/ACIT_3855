from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class UserWeight(Base):
    """ User Weight """

    __tablename__ = "user_weight"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    weight_kg = Column(Integer, nullable=False)
    weight_lbs = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, user_id, weight_kg, weight_lbs, timestamp, trace_id):
        """ Initializes a user weight reading """
        self.user_id = user_id
        self.weight_kg = weight_kg
        self.weight_lbs = weight_lbs
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a user weight reading """
        dict = {}
        dict['id'] = self.id
        dict['user_id'] = self.user_id
        dict['weight_kg'] = self.weight_kg
        dict['weight_lbs'] = self.weight_lbs
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict