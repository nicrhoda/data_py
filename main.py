# imports required
import pyodbc
import random
from decouple import config

# connection params for ms access
driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
db_file = config(r"db_file")  

# connecting to ms access db and creating cursor to navigate access db (also works for sql)
connection_string = f'DRIVER={driver};DBQ={db_file};'
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# create the table with id and various other fields with specified data types
table_creation_query = """
CREATE TABLE SensorData (
    id AUTOINCREMENT PRIMARY KEY,
    temperature_one INT,
    humidity_one INT,
    temperature_two INT,
    humidity_two INT
);
"""
cursor.execute(table_creation_query)
# commits changes to access to fully create table
connection.commit()

# loop to create random data between 70-90 for each field of each row
for i in range(1, 200):
    temperature_one = random.randint(70, 90)
    humidity_one = random.randint(70, 90)
    temperature_two = random.randint(70, 90)
    humidity_two = random.randint(70, 90)

    insert_query = f"INSERT INTO SensorData (temperature_one, humidity_one, temperature_two, humidity_two) " \
                   f"VALUES ({temperature_one}, {humidity_one}, {temperature_two}, {humidity_two});"

    cursor.execute(insert_query)
    # commits on each loop one by one
    connection.commit()

# closing connections
cursor.close()
connection.close()

print("Table created and populated with data.")
