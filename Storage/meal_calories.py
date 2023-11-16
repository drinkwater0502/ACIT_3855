from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class MealCalories(Base):
    """ Meal Calories """

    __tablename__ = "meal_calories"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    calorie_count = Column(Integer, nullable=False)
    meal_name = Column(String(250), nullable=False)
    meal_number = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, user_id, calorie_count, meal_name, meal_number, timestamp, trace_id):
        """ Initializes a meal calories reading """
        self.user_id = user_id
        self.calorie_count = calorie_count
        self.meal_name = meal_name
        self.meal_number =  meal_number
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a meal calories reading """
        dict = {}
        dict['id'] = self.id
        dict['user_id'] = self.user_id
        dict['calorie_count'] = self.calorie_count
        dict['meal_name'] = self.meal_name
        dict['meal_number'] = self.meal_number
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict