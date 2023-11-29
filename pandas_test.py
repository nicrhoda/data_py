# imports
import pyodbc
import pandas as pd
from datetime import datetime
from decouple import config
# make sure to install xlsxwriter (pandas sometimes will not include it)

# connection params to ms access
driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
db_file = config(r"db_file")  

# connects to access db and table
connection_string = f'DRIVER={driver};DBQ={db_file};'
connection = pyodbc.connect(connection_string)

# sql query to gather all of the data from SensorData table
query = "SELECT * FROM SensorData;"

# df = data frame, giving pandas all of the data from the table
df = pd.read_sql_query(query, connection)

# pandas calculating the averages of all of the columns
# the columns are stored in an array and the .mean() method is applied to them
avg_temperature_one = df['temperature_one'].mean()
avg_humidity_one = df['humidity_one'].mean()
avg_temperature_two = df['temperature_two'].mean()
avg_humidity_two = df['humidity_two'].mean()

# averages are pulled into new data frame
averages_df = pd.DataFrame({
    'Average Temperature One': [avg_temperature_one],
    'Average Humidity One': [avg_humidity_one],
    'Average Temperature Two': [avg_temperature_two],
    'Average Humidity Two': [avg_humidity_two]
})

# get the current date to name the new excel file
current_date = datetime.now().strftime('%Y-%m-%d')
excel_file_name = f'Averages_{current_date}.xlsx'

# creating the excel file and writing the data to it
with pd.ExcelWriter(excel_file_name, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='SensorData', index=False)
    averages_df.to_excel(writer, sheet_name='Averages', index=False)

# closes connection to db
connection.close()

print(f"Excel file '{excel_file_name}' created with data from SensorData and averages.")
