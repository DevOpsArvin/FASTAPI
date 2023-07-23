import sqlite3
import datetime

def create_database():
    """Creates the database file if it does not exist."""
    try:
        conn2 = sqlite3.connect('elog.db')
    except sqlite3.Error as e:
        print(e)
        print('Creating database...')
        conn2 = sqlite3.connect('elog.db')
    return conn2

def create_table(conn2):
    """Creates a table in the database."""
    c = conn2.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS eventlog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datestamp TEXT,
                    indexrow TEXT,
                    station TEXT,
                    host TEXT,
                    interface TEXT,
                    floor TEXT,
                    location TEXT,
                    actions TEXT,
                    doneby TEXT
                )''')


def insert_data(conn2, data):
    """Inserts data into the table."""
    c = conn2.cursor()
    c.execute('INSERT INTO eventlog (datestamp, indexrow, station, host, interface, floor, location, actions, doneby) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    conn2.commit()

def main():
    conn2 = create_database()
    create_table(conn2)


    # Get the current date and time.
    now = datetime.datetime.now()

    # Convert the date and time to a string.
    datestamp = now.strftime('%Y-%m-%d %H:%M:%S')


    # Sample data
    data = (datestamp, '1', 'StationA', 'HostA', 'InterfaceA', 'Floor1', 'LocationA', 'ActionA', 'UserA')

    insert_data(conn2, data)

    # Close the connection.
    conn2.close()

if __name__ == '__main__':
    main()
