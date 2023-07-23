import datetime
import csv
import os


# Check if the CSV file exists.
if not os.path.exists('my_csv_file.csv'):

    # Create a list of headers.
    headers = [
        'datestamp', 'indexrow', 'station', 'host', 'interface', 'floor', 'location', 'actions', 'doneby',
    ]

    # Create a blank CSV file.
    with open('my_csv_file.csv', 'w', newline='') as csvfile:

        # Create a CSV writer object.
        writer = csv.writer(csvfile, delimiter=',')

        # Write the headers to the CSV file.
        writer.writerow(headers)




data = []

# Get the current date and time.
now = datetime.datetime.now()

# Convert the date and time to a string.
datestamp = now.strftime('%Y-%m-%d %H:%M:%S')

# Get the user input.
indexrow = input('Enter indexrow: ')
station = input('Enter station: ')
host = input('Enter host: ')
interface = input('Enter interface: ')
floor = input('Enter floor: ')
location = input('Enter location: ')
actions = input('Enter actions: ')
doneby = input('Enter doneby: ')

# Add the user input to the data list.
data.append([datestamp, indexrow, station, host, interface, floor, location, actions, doneby])

# Open the CSV file in append mode.
with open('my_csv_file.csv', 'a', newline='') as csvfile:

    # Create a CSV writer object.
    writer = csv.writer(csvfile, delimiter=',')

    # Write the data to the CSV file.
    writer.writerows(data)
