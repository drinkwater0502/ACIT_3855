import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from meal_calories import MealCalories
from user_weight import UserWeight
import datetime
# import mysql-connector-python
import pymysql
import yaml
import logging
import logging.config

import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

user = app_config['datastore']['user']
password = app_config['datastore']['password']
hostname = app_config['datastore']['hostname']
port = app_config['datastore']['port']
db = app_config['datastore']['db']

DB_ENGINE = create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info(f"Connecting to DB. Hostname: {hostname}, Port: {port}")

# Your functions here
# def meal_calories(body):
#     session = DB_SESSION()

#     mc = MealCalories(body['user_id'],
#                        body['calorie_count'],
#                        body['meal_name'],
#                        body['meal_number'],
#                        body['timestamp'],
#                        body['trace_id'])

#     session.add(mc)
#     session.commit()
#     session.close()

#     logger.debug(f'Stored event meal_calories request with a trace_id of {body["trace_id"]}')

#     return NoContent, 201

# def user_weight(body):
#     session = DB_SESSION()

#     uw = UserWeight(body['user_id'],
#                        body['weight_kg'],
#                        body['weight_lbs'],
#                        body['timestamp'],
#                        body['trace_id'])

#     session.add(uw)
#     session.commit()
#     session.close()

#     logger.debug(f'Stored event user_weight request with a trace_id of {body["trace_id"]}')

#     return NoContent, 201

def get_meal_calories(timestamp):

    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    readings = session.query(MealCalories).filter(MealCalories.date_created >= timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    
    session.close()

    logger.info("Query for Meal Calories after %s returns %d results" % (timestamp, len(results_list)))

    return results_list, 200

def get_user_weight(timestamp):

    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    readings = session.query(UserWeight).filter(UserWeight.date_created >= timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    
    session.close()

    logger.info("Query for User Weight after %s returns %d results" % (timestamp, len(results_list)))

    return results_list, 200

def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
    reset_offset_on_start=False,
    auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "calories": # Change this to your event type
        # Store the event1 (i.e., the payload) to the DB
            session = DB_SESSION()
            mc = MealCalories(payload['user_id'],
                            payload['calorie_count'],
                            payload['meal_name'],
                            payload['meal_number'],
                            payload['timestamp'],
                            payload['trace_id'])
            session.add(mc)
            session.commit()
            session.close()
        elif msg["type"] == "weight": # Change this to your event type
        # Store the event2 (i.e., the payload) to the DB
        # Commit the new message as being read
            session = DB_SESSION()
            uw = UserWeight(payload['user_id'],
                            payload['weight_kg'],
                            payload['weight_lbs'],
                            payload['timestamp'],
                            payload['trace_id'])
            session.add(uw)
            session.commit()
            session.close()
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation = True, validate_responses = True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
