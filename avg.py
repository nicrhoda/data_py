# imports required
import pyodbc
from sms import main
from decouple import config

# connection params to ms access
driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
db_file = config(r"db_file")

# establishinh connection to access db
connection_string = f'DRIVER={driver};DBQ={db_file};'
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# sql style query to gather the averages from every row
average_query = """
SELECT
    AVG(temperature_one) AS avg_temperature_one,
    AVG(humidity_one) AS avg_humidity_one,
    AVG(temperature_two) AS avg_temperature_two,
    AVG(humidity_two) AS avg_humidity_two
FROM
    SensorData;
"""

# executes the query
cursor.execute(average_query)

# fetches the average one by one to store as variables and makes them more readable
result = cursor.fetchone()

# averages stored as variables and printed
avg_temperature_one = result.avg_temperature_one
avg_humidity_one = result.avg_humidity_one
avg_temperature_two = result.avg_temperature_two
avg_humidity_two = result.avg_humidity_two

print(f"Average Temperature One: {avg_temperature_one:.2f}")
print(f"Average Humidity One: {avg_humidity_one:.2f}")
print(f"Average Temperature Two: {avg_temperature_two:.2f}")
print(f"Average Humidity Two: {avg_humidity_two:.2f}")

# sends text message containing all of the averages using the sms script
inputmessage = (f"Average Sensor One Temp: {avg_temperature_one:.2f} Humidity: {avg_humidity_one:.2f}.  Average Sensor Two Temp: {avg_temperature_two:.2f}, Humidity: {avg_humidity_two:.2f}")
main(inputmessage)

# closing connections
cursor.close()
connection.close()
