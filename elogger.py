import sqlite3
import datetime

def create_database():
    """Creates the database file if it does not exist."""
    try:
        conn = sqlite3.connect('elog.db')
    except sqlite3.Error as e:
        print(e)
        print('Creating database...')
        conn = sqlite3.connect('elog.db')
    return conn

def create_table(conn):
    """Creates a table in the database."""
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS eventlog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datestamp TEXT,
                    indexrow INTEGER,
                    station TEXT,
                    host TEXT,
                    interface TEXT,
                    floor TEXT,
                    location TEXT,
                    actions TEXT,
                    doneby TEXT
                )''')

def insert_data(conn, data):
    """Inserts data into the table."""
    c = conn.cursor()
    c.execute('INSERT INTO eventlog (datestamp, indexrow, station, host, interface, floor, location, actions, doneby) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()

def main():
    conn = create_database()
    create_table(conn)


    # Get the current date and time.
    now = datetime.datetime.now()

    # Convert the date and time to a string.
    datestamp = now.strftime('%Y-%m-%d %H:%M:%S')


    # Sample data
    data = (datestamp, 1, 'StationA', 'HostA', 'InterfaceA', 'Floor1', 'LocationA', 'ActionA', 'UserA')

    insert_data(conn, data)

    # Close the connection.
    conn.close()

if __name__ == '__main__':
    main()
