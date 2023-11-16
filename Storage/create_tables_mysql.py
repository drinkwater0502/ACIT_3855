import mysql.connector
db_conn = mysql.connector.connect(host="ec2-34-215-184-146.us-west-2.compute.amazonaws.com", user="user", password="password", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
          CREATE TABLE meal_calories
          (id INT NOT NULL AUTO_INCREMENT, 
           user_id VARCHAR(250) NOT NULL,
           calorie_count INTEGER NOT NULL,
           meal_name VARCHAR(250) NOT NULL,
           meal_number INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(250) NOT NULL,
           CONSTRAINT meal_calories_pk PRIMARY KEY (id))
          ''')
db_cursor.execute('''
          CREATE TABLE user_weight
          (id INT NOT NULL AUTO_INCREMENT, 
           user_id VARCHAR(250) NOT NULL,
           weight_kg INTEGER NOT NULL,
           weight_lbs INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(250) NOT NULL,
           CONSTRAINT user_weight_pk PRIMARY KEY (id))
          ''')
db_conn.commit()
db_conn.close()