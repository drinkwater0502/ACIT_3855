import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE meal_calories
          (id INTEGER PRIMARY KEY ASC, 
           user_id VARCHAR(250) NOT NULL,
           calorie_count INTEGER NOT NULL,
           meal_name VARCHAR(250) NOT NULL,
           meal_number INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(250) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE user_weight
          (id INTEGER PRIMARY KEY ASC, 
           user_id VARCHAR(250) NOT NULL,
           weight_kg INTEGER NOT NULL,
           weight_lbs INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(250) NOT NULL)
          ''')

conn.commit()
conn.close()