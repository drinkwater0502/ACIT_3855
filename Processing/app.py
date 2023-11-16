import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pymysql
import yaml
import logging
import logging.config
import requests
import sqlite3

import datetime

from apscheduler.schedulers.background import BackgroundScheduler
import json

with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

# def get_stats():
#     print('DATETIME LOOK HERE', type(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#     session = DB_SESSION()
#     results = session.query(Stats).order_by(Stats.last_updated.desc()) #2000-02-10T13:00:00Z datetime format for stats

#     con = sqlite3.connect("stats.sqlite")
#     cur = con.cursor()
#     cur.execute(str(results))
#     result = cur.fetchall()

#     con.close()
#     session.close()
    
#     if len(result) == 0:
#         print('EMPTY')
#         return 'empty'
    
#     return result[0]
    # [(column1, column2), (), ()]
    
    
# def populate_sstats():
    # all_stats = get_stats()
    # if all_stats == 'empty':
    #     last_updated_stats = '2000-02-10T13:00:00Z'
    #     curr_total_purchased_tickets = 0
    #     curr_total_registered_concerts = 0
    #     curr_highest_ticket_price = 0
    #     curr_lowest_ticket_price = 0
    #     curr_youngest_ticket_buyer = 0
    # else:
    #     last_updated_stats = all_stats[6]
    #     curr_total_purchased_tickets = all_stats[1]
    #     curr_total_registered_concerts = all_stats[2]
    #     curr_highest_ticket_price = all_stats[3]
    #     curr_lowest_ticket_price = all_stats[4]
    #     curr_youngest_ticket_buyer = all_stats[5]

    
    # logger.info("Start Periodic Processing")
    
    # num_events = 0
    # req = requests.get(f'http://127.0.0.1:8090/concerts/register?timestamp={last_updated_stats}')
    # if req.status_code != 200:
    #     logger.error("Status code was not 200 for register endpoint")
    # for obj in req.json():
    #     num_events += 1
    #     concerts.append(obj)
    #     logger.debug(f'Processed register event with trace id {obj["trace_id"]}')
    
    # req = requests.get(f'http://127.0.0.1:8090/concerts/buy?timestamp={last_updated_stats}')
    # if req.status_code != 200:
    #     logger.error("Status code was not 200 for buy endpoint")
    # for obj in req.json():
    #     num_events += 1
    #     tickets.append(obj)
    #     ticket_prices.append(obj['ticket_price'])
    #     ages.append(obj['user_age'])
    #     logger.debug(f'Processed buy event with trace id {obj["trace_id"]}')
    
    # logger.info(f"Received {num_events} in total between the Buy and Register endpoints")
    
    # highest_ticket_price_endpoint = max(ticket_prices)
    # lowest_ticket_price_endpoint = min(ticket_prices)
    # youngest_ticket_buyer_endpoint = min(ages)

    # logger.debug(f"New Number of Tickets: {len(tickets)}")
    # logger.debug(f"New Number of Concerts: {len(concerts)}")
    # if highest_ticket_price_endpoint > curr_highest_ticket_price:
    #     highest_to_send = highest_ticket_price_endpoint
    #     logger.debug(f"New Highest Ticket Price: {highest_to_send}")
    # else: 
    #     highest_to_send = curr_highest_ticket_price
    
    # if lowest_ticket_price_endpoint < curr_lowest_ticket_price:
    #     lowest_to_send = lowest_ticket_price_endpoint
    #     logger.debug(f"New Lowest Ticket Price: {lowest_to_send}")
    # else:
    #     lowest_to_send = curr_lowest_ticket_price

    # if youngest_ticket_buyer_endpoint < curr_youngest_ticket_buyer:
    #     youngest_to_send = youngest_ticket_buyer_endpoint
    #     logger.debug(f"New Youngest Ticket Buyer: {youngest_to_send}")
    # else:
    #     youngest_to_send = curr_youngest_ticket_buyer

    # session = DB_SESSION()
    # curr_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    # datetime_curr_time = datetime.datetime.strptime(curr_time, "%Y-%m-%dT%H:%M:%SZ")

    # stats = Stats(len(tickets),
    #             len(concerts),
    #             highest_to_send,
    #             lowest_to_send,
    #             youngest_to_send,
    #             datetime_curr_time)
    # session.add(stats)
    # session.commit()
    # session.close()

    # logger.info("Period Processing Finished")

def get_stats():
    logger.info('Getting stats')
    try:
        file_handle = open(app_config['datastore']['filename'], 'r')
        file_contents = file_handle.read()
        python_data = json.loads(file_contents) #convert json string to python data (array)
        file_handle.close()
        logger.debug(f'{python_data}')
        logger.info('Get stats request completed')
        return python_data, 200
    except FileNotFoundError:
        logger.error('data.json file does not exist')
        return 'Statistics do not exist', 404


def populate_stats():
    logger.info("Periodic processing has started")
    r = requests.get('http://localhost:8100/stats')
    if r.status_code == 404:
        # default values
        old_stats = {
            'last_updated_stats': '2000-02-10T13:00:00Z',
            'total_meal_calorie_entries': 0,
            'total_user_weight_entries': 0,
            'highest_meal_calorie': 0,
            'lowest_user_weight': 9999
        }
    else:
        old_stats = r.json()
    
    curr_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    r_calories = requests.get(f'http://localhost:8090/calories?timestamp={old_stats["last_updated_stats"]}')
    r_weight = requests.get(f'http://localhost:8090/weight?timestamp={old_stats["last_updated_stats"]}')
    if r_calories.status_code != 200 or r_weight.status_code != 200:
        logger.error('get request for timestamp failed')
    else:
        num_calories_events = 0
        num_weight_events = 0
        for events in r_calories.json():
            num_calories_events += 1
        for events in r_weight.json():
            num_weight_events += 1
        logger.info(f'Received {num_calories_events} meal calorie events and {num_weight_events} user weight events')

        new_stats = {
            'last_updated_stats': curr_time,
            'total_meal_calorie_entries': old_stats['total_meal_calorie_entries'] + num_calories_events,
            'total_user_weight_entries': old_stats['total_user_weight_entries'] + num_weight_events,
            'highest_meal_calorie': old_stats['highest_meal_calorie'],
            'lowest_user_weight': old_stats['lowest_user_weight']
        }

        if len(r_calories.json()) != 0:
            calorie_counts = [entry['calorie_count'] for entry in r_calories.json()]
            max_calorie_count = max(calorie_counts)
            if max_calorie_count > new_stats['highest_meal_calorie']:
                new_stats['highest_meal_calorie'] = max_calorie_count

        if len(r_weight.json()) != 0:
            weight_counts = [entry['weight_kg'] for entry in r_weight.json()]
            min_weight_count = min(weight_counts)
            if min_weight_count < new_stats['lowest_user_weight']:
                new_stats['lowest_user_weight'] = min_weight_count

        with open(app_config['datastore']['filename'], 'w') as json_file:
            json.dump(new_stats, json_file)
        
        logger.debug(new_stats)
    logger.info('Period processing has ended')

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)