import mysql.connector
db_conn = mysql.connector.connect(host="localhost", user="root", password="password", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
                DROP TABLE meal_calories, user_weight
                ''')
db_conn.commit()
db_conn.close()