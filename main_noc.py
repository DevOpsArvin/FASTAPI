from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.responses import RedirectResponse
from fastapi import Response

from contextlib import closing

from fastapi import Response

import sqlite3
import datetime





#import textwrap
#import html


import netmiko
from netmiko.ssh_exception import NetmikoTimeoutException, SSHException, AuthenticationException
from netmiko import ConnectHandler  # Import the ConnectHandler class


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

# Initialize templates
templates = Jinja2Templates(directory="templates")

UsersLoggedIn = {}  # Define the UsersLoggedIn dictionary


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Connect to the SQLite database using a context manager
def get_database_connection():
    conn = sqlite3.connect("epmap.db")
    return conn


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def create_database():
    """Creates the database file if it does not exist."""
    try:
        conn2 = sqlite3.connect('elog.db')
    except sqlite3.Error as e:
        print(e)
        print('Creating database...')
        conn2 = sqlite3.connect('elog.db')
    return conn2

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def insert_data(conn2, data):
    """Inserts data into the table."""
    c = conn2.cursor()
    c.execute('INSERT INTO eventlog (datestamp, indexrow, station, host, interface, floor, location, actions, doneby) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    conn2.commit()



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class XUser:
    def __init__(self, username, password, hostname):
        self.username = username
        self.password = password
        self.hostname = hostname

    def cisco(self):
        cisco = {
            'device_type': 'cisco_ios',
            'username': f'{self.username}',
            'password': f"{self.password}",
            'host': f'{self.hostname}'
        }
        return cisco


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NetmikoManager:
    def __init__(self, hostname, username, password):
        self.cisco = {
            "device_type": "cisco_ios",
            "host": hostname,
            "username": username,
            "password": password,
        }
        self.ssh_connection = None

    def connect(self):
        try:
            self.ssh_connection = ConnectHandler(**self.cisco)
        except netmiko.ssh_exception.AuthenticationException as e:
            err = """
            Authentication Error: Invalid username and password
            """
            return err
            #return False , err

        except netmiko.ssh_exception.NetmikoTimeoutException as e:
            print(f"Timeout to device: {e}")
            err = e
            
            return err
            #return False , err

        except netmiko.ssh_exception.NetmikoAuthenticationException as e:
            print(f"SSH connection error: {e}")
            err = e
            
            return err
            #return False , err

        except Exception as e:
            print(f"An error occurred: {e}")
            err = e
            
            return err
            #return False , err

        
        #return True

        

    def disconnect(self):
        if self.ssh_connection:
            self.ssh_connection.disconnect()
            self.ssh_connection = None

    def doit(self, interface, config_commands):
        if not self.ssh_connection:
            print("SSH connection is not established. Call the connect() method first.")
            return

        try:
            # Send configuration commands using send_config_set()
            output = self.ssh_connection.send_config_set(config_commands)

            # Print the output of the configuration commands
            print(output)

        except Exception as e:
            print(f"An error occurred: {e}")




#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TokenAccount:
    instances = {}

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.instances[username] = self

    def get_account(self, username):
        return self.instances.get(username)

    def create_account(self, username, password):
        return TokenAccount(username, password)

    def delete_account(self, username):
        if username in self.instances:
            del self.instances[username]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def perform_search(query):
    conn = sqlite3.connect("epmap.db")
    cursor = conn.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_mapping_results(station):
    query = f"SELECT * FROM mapping WHERE station LIKE '%{station}%'"
    results = perform_search(query)
    return results

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_vlan_results():
    query = f"SELECT * FROM vlans"
    results = perform_search(query)
    return results

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_voice_results():
    query = f"SELECT * FROM voices"
    results = perform_search(query)
    return results


#===================================================================
@app.get("/")
async def home(request: Request):
    print("+++++++++++++++++++++++++++++++++++")
    print(f"Number of User Logged-in to the System : {len(UsersLoggedIn)}")
    print("+  User is preparing to Login...  +")
    print("+++++++++++++++++++++++++++++++++++")
    conn2 = create_database()
    create_table(conn2)
    print("STARTING WEB APP")
    return templates.TemplateResponse("login.html", {"request": request})


userValid = False

#===================================================================
@app.post("/xlogin")
async def process_login(
        request: Request, 
        username: str = Form(...), 
        password: str = Form(...)
        ):

    if (username == "aa" and password == "aa") or (username == "bb" and password == "bb") or (username == "cc" and password == "cc"):
        userValid = True
        connection_result = None
    else:    
        userValid = False
        connection_result = "ERROR : Username & Password.."

    err = None
            
    print(f"360: {userValid}")
    print(f"361: {connection_result}")


    

    if userValid == True:

        # Add the logged-in user to UsersLoggedIn dictionary
        UsersLoggedIn[username] = TokenAccount(username, password)

        # Print all account instances
        for account_instance in TokenAccount.instances.values():
            print(f"73=======: {account_instance.username} {account_instance.password}")

            loginUsr = f"Account {account_instance.username} is accessing to Login... +"
            print(f"+  {loginUsr}")
            print(f"Number of User Logged-in to the System : {len(UsersLoggedIn)}")

        account_instance = UsersLoggedIn.get(username)
        if account_instance:
            password = account_instance.password
            print(f"368 =======: {username} {password}")
            print(f"User :{username} STATUS: LOGGED IN")
            
        else:
            print("Account not found.")


        print(f"374 -- Error : {err}") 

        return templates.TemplateResponse(
            "search.html", 
            {   "request": request, 
                "loginU_var": username
            }
        )
    else:    
        print(f"377 Error : {err}") 
        return templates.TemplateResponse(
            "login.html", 
            {
                "request": request, 
                "error_message": connection_result
            }
        )


#===================================================================
@app.post("/login")
async def process_login(
        request: Request, 
        username: str = Form(...), 
        password: str = Form(...)
        ):

    # Device information

    hostname = "10.16.0.80"
    #hostname = "sandbox-iosxr-1.cisco.com"

    #username = 'admin'
    #password = 'C1sco12345'

    #username = 'a.acosta'
    #password = '!@Rvin#8569'

    
    netmiko_manager = NetmikoManager(hostname, username, password)
    print(f"270 ---{netmiko_manager.connect()}")
    print(f"271 ---{netmiko_manager}")

    err = None
    userValid = netmiko_manager.connect() is None or False


    if userValid == True:

        # Add the logged-in user to UsersLoggedIn dictionary
        UsersLoggedIn[username] = TokenAccount(username, password)

        # Print all account instances
        for account_instance in TokenAccount.instances.values():
            print(f"73=======: {account_instance.username} {account_instance.password}")

            loginUsr = f"Account {account_instance.username} is accessing to Login... +"
            print(f"+  {loginUsr}")
            print(f"Number of User Logged-in to the System : {len(UsersLoggedIn)}")

        account_instance = UsersLoggedIn.get(username)
        if account_instance:
            password = account_instance.password
            print(f"297 =======: {username} {password}")
            print(f"User :{username} STATUS: LOGGED IN")
            
        else:
            print("Account not found.")


        print(f"303 -- Error : {err}") 

        return templates.TemplateResponse(
            "search.html", 
            {   "request": request, 
                "loginU_var": username
            }
        )
    else:    
        print(f"312 Error : {err}") 
        return templates.TemplateResponse(
            "login.html", 
            {
                "request": request, 
                "error_message": netmiko_manager.connect()
                #[1] #get the 2nd arg.
            }
        )



#===================================================================
@app.post("/search")
async def search(
        request: Request, 
        station: str = Form(...), 
        loginU_var: str = Form(...)
        ):

    # Connect to the SQLite database
    results = get_mapping_results(station)
    resultsVLAN = get_vlan_results()
    resultsVoice = get_voice_results()

    print(results[0])
    print(results)

    #view_modal = modal_selectedRow(idrow,station,port,interface,floor,location)

    # Pass the results, search input, and loginU_var to the template
    if len(UsersLoggedIn) != 0:
        return templates.TemplateResponse(
            "search.html",
            {   "request": request, 
                "results": results, 
                "station": station, 
                "loginU_var": loginU_var,
                "resultsVLAN": resultsVLAN,
                "resultsVoice": resultsVoice, 
                #"viewModal": viewModal
            }
        )
    else:
        print("You must login first.")
        return templates.TemplateResponse("login.html", {"request": request})


#===================================================================
def process_request(hostname, username, password,interface, config_commands):
    netmiko_manager = NetmikoManager(hostname, username, password)
    netmiko_manager.connect()
    
    netmiko_manager.doit(interface, config_commands)
    netmiko_manager.disconnect()


#===================================================================
@app.post("/process_modal_form1")
async def process_modal_form(
                request: Request, 
                loginU_var: str = Form(...),   
                idrow: str = Form(...),
                floor: str = Form(...),
                station: str = Form(...),                           
                port: str = Form(...), 
                interface: str = Form(...),
                location: str = Form(...)
                ):
    

    print("==========================================================")
    print("Process: CLEAR PORT")
    print("-----------------")
    print("ID:", idrow)
    print("Station:", station)
    print("Port:", port)
    print("Interface:", interface)
    print("Floor:", floor)
    print("Location:", location)
    print("-----------------")
    print("Clear Port Performed by :", loginU_var)
    print("==========================================================")


    username = loginU_var
    account_instance = UsersLoggedIn.get(username)
    if account_instance:
        password = account_instance.password
    else:
        print("Account not found.")

    print("--------------------------")
    print("USER PASSWORD:", password)
    print("--------------------------")


    #result = login(username, password)
    print(f"CLEAR PORT CODE HERE....")

    hostname = f"10.16.0.{port}"
    username = loginU_var
    password = password
    interface = interface
    
    print(f"420 ---  {hostname}")

    # Clear Port
    config_commands = [
        f"interface {interface}",
        "shutdown",
        "no shutdown",
        "exit",  # Exit interface configuration mode
    ]

    # Do Clear Port
    process_request(hostname, username, password, interface, config_commands)

    
    # Get the current date and time.--------------------------------------------
    now = datetime.datetime.now()

    # Convert the date and time to a string.
    datestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    # Sample data
    data = (datestamp, idrow, station, hostname, interface, floor, location, 'CLEAR PORT', loginU_var)
    
    conn2 = sqlite3.connect('elog.db')
    cursor = conn2.cursor()
    c = conn2.cursor()
    c.execute('INSERT INTO eventlog (datestamp, indexrow, station, host, interface, floor, location, actions, doneby) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', data)

    conn2.commit()

    # Close the connection.
    conn2.close()
    #--------------------------------------------------------------------------



    results = get_mapping_results(station)
    resultsVLAN = get_vlan_results()
    resultsVoice = get_voice_results()

    # Process the form data as needed
    return templates.TemplateResponse(
        "search.html",
        {   "request": request, 
            "results": results, 
            "idrow": idrow, 
            "floor": floor, 
            "station": station, 
            "port": port, 
            "interface": interface, 
            "loginU_var": loginU_var,
            "resultsVLAN": resultsVLAN,
            "resultsVoice": resultsVoice

        }

    )




#===================================================================
@app.post("/process_modal_form2")
async def process_modal_form(
                request: Request,
                loginU_var: str = Form(...),  
                idrow: str = Form(...),
                floor: str = Form(...),
                station: str = Form(...),
                port: str = Form(...), 
                interface: str = Form(...),
                location: str = Form(...),
                VLANCustom: str = Form(...)
                ):

    print("==========================================================")
    print("Process: Change VLAN")
    print("-----------------")
    print("ID:", idrow)
    print("Station:", station)
    print("Port:", port)
    print("Interface:", interface)
    print("Floor:", floor)
    print("Location:", location)
    print("Change to VLAN:", VLANCustom)
    print("-----------------")
    print("Change VLAN Performed by :", loginU_var)
    print("==========================================================")
    

    username = loginU_var
    if UsersLoggedIn.get(username):
        password = UsersLoggedIn.get(username).password
        #print(f"line116=======: {username} {password}")
    else:
        print("Account not found.")


    print(f"CHANGE VLAN CODE HERE....")

    hostname = f"10.16.0.{port}"
    username = loginU_var
    password = password
    interface = interface
    vlanID = VLANCustom
    
    print(f"504 ---  {hostname}")
    print(f"505 ---  {VLANCustom}")

    # Clear Port
    config_commands = [
        f"interface {interface}",
        f"switchport access vlan {vlanID}",
        "shutdown",
        "no shutdown",
        "end",  # Exit interface configuration mode
    ]

    process_request(hostname, username, password, interface, config_commands)

    results = get_mapping_results(station)
    resultsVLAN = get_vlan_results()
    resultsVoice = get_voice_results()

    # Process the form data as needed

    return templates.TemplateResponse(
        "search.html",
        {   "request": request, 
            "results": results, 
            "idrow": idrow, 
            "floor": floor, 
            "station": station, 
            "port": port, 
            "interface": interface, 
            "loginU_var": loginU_var,
            "resultsVLAN": resultsVLAN,
            "resultsVoice": resultsVoice           
        }
    )





#===================================================================
@app.post("/process_modal_form3")
async def process_modal_form(
                request: Request,
                loginU_var: str = Form(...),  
                idrow: str = Form(...),
                floor: str = Form(...),
                station: str = Form(...),
                port: str = Form(...), 
                interface: str = Form(...),
                VoiceCustom: str = Form(...)
                ):



    print("==========================================================")
    print("Process: Change Voice")
    print("-----------------")
    print("ID:", idrow)
    print("Station:", station)
    print("Port:", port)
    print("Interface:", interface)
    print("Floor:", floor)
    print("Location:", location)
    print("Change to Voice:", VoiceCustom)
    print("-----------------")
    print("Change Voice Performed by :", loginU_var)
    print("==========================================================")


    username = loginU_var
    if UsersLoggedIn.get(username):
        password = UsersLoggedIn.get(username).password
        print(f"line116=======: {username} {password}")
    else:
        print("Account not found.")

    results = get_mapping_results(station)
    resultsVLAN = get_vlan_results()
    resultsVoice = get_voice_results()

    # Process the form data as needed

    return templates.TemplateResponse(
        "search.html",
        {   "request": request, 
            "results": results, 
            "idrow": idrow, 
            "station": station, 
            "port": port, 
            "interface": interface, 
            "loginU_var": loginU_var,
            "resultsVLAN": resultsVLAN,
            "resultsVoice": resultsVoice           
        }
    )





#===================================================================
if __name__ == "__main__":
    import uvicorn



    uvicorn.run(app, host="0.0.0.0", port=8886)

    #uvicorn.run(app, host="0.0.0.0", port=8886)
#   uvicorn main:app --reload --host 0.0.0.0 --port 8886
# arvin 7/15/2023
