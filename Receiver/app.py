import connexion
from connexion import NoContent
import json
import datetime
import requests
import yaml
import logging
import logging.config
import uuid
from pykafka import KafkaClient
import time
import os

MAX_EVENTS = 10
EVENT_FILE = 'events.json'

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, "r") as f:
    app_config = yaml.safe_load(f.read())

with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

hostname = app_config['events']['hostname']
port = app_config['events']['port']
retries = app_config['retries']['max']
wait_time = app_config['retries']['sleep']
counter = 0
while counter < retries:
    logger.info(f'Trying to connect to Kafka, try number {counter}')
    try:
        client = KafkaClient(hosts=f"{hostname}:{port}")
        topic = client.topics[str.encode(app_config['events']['topic'])]
        producer = topic.get_sync_producer()
        break

    except:
            logger.error('Error while trying to connect to Kafka')
            counter += 1
            time.sleep(wait_time)


# Your functions here
def meal_calories(body):

    trace_id = str(uuid.uuid4())

    body['trace_id'] = trace_id

    logger.info(f'Received event meal_calories request with a trace id of {trace_id}')

    # headers = {'Content-Type': 'application/json'}
    # r = requests.post(app_config['eventstore1']['url'], json=body, headers=headers)
    # print(r.status_code)
    # client = KafkaClient(hosts=f'{hostname}:{port}')
    # topic = client.topics[str.encode(app_config['events']['topic'])]
    # producer = topic.get_sync_producer()
    msg = { "type": "calories",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body }
    logger.info(msg)
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))


    logger.info(f'Returned event meal_calories response (Id: {trace_id}) with status 201')

    return NoContent, 201

def user_weight(body):

    trace_id = str(uuid.uuid4())

    body['trace_id'] = trace_id

    logger.info(f'Received event user_weight request with a trac id of {trace_id}')

    # headers = {'Content-Type': 'application/json'}
    # r = requests.post(app_config['eventstore2']['url'], json=body, headers=headers)
    # print(r.status_code)
    # client = KafkaClient(hosts=f'{hostname}:{port}')
    # topic = client.topics[str.encode(app_config['events']['topic'])]
    # producer = topic.get_sync_producer()
    msg = { "type": "weight",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f'Returned event user_weight response (Id: {trace_id}) with status 201')

    return NoContent, 201

def update_events_json(string_data):
    file_handle = open(EVENT_FILE, 'r')
    file_contents = file_handle.read()
    python_data = json.loads(file_contents) #convert json string to python data (array)
    file_handle.close()

    if len(python_data) >= MAX_EVENTS: # if more than 10 events stored, delete the oldest event
        python_data = python_data[:-1]

    event_object = {}
    current_datetime = datetime.datetime.now()
    current_datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
    event_object['received_timestamp'] = current_datetime_string
    event_object['request_data'] = string_data
    
    python_data.insert(0, event_object) # append new dictionary to front of array

    json_str = json.dumps(python_data) # convert python data to json string
    file_handle = open(EVENT_FILE, "w")
    file_handle.write(json_str)
    file_handle.close()

def get_health():
    return 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", base_path="/receiver", strict_validation = True, validate_responses = True)

if __name__ == "__main__":
    app.run(port=8080)