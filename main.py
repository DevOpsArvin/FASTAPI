from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.responses import RedirectResponse
from fastapi import Response

from contextlib import closing

from fastapi import Response

import textwrap

import sqlite3

from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

# Initialize templates
templates = Jinja2Templates(directory="templates")

UsersLoggedIn = {}  # Define the UsersLoggedIn dictionary

#loginU_var = ""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Connect to the SQLite database using a context manager
def get_database_connection():
    conn = sqlite3.connect("epmap.db")
    return conn

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
def xvalidate_login(username, password, device, commands):
    result = {}
    try:

        username = device["username"]
        password = device["password"]

        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output

        print("Login Successfull - Proceed to Search")
        print(f"66=======: {username} {password}")

        # Add the logged-in user to UsersLoggedIn dictionary
        UsersLoggedIn[username] = TokenAccount(username, password)

        # Print all account instances
        for account_instance in TokenAccount.instances.values():
            print(f"73=======: {account_instance.username} {account_instance.password}")

        print(f"length ====== {len(UsersLoggedIn)}")

        account_instance = UsersLoggedIn.get(username)
        if account_instance:
            password = account_instance.password
            print(f"79=======: {username} {password}")
        else:
            print("Account not found.")


        return True

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
        return False, str(error)


def validate_login(username, password, device, commands):
    try:
        if (username == "aa" and password == "aa") or (username == "bb" and password == "bb") or (username == "cc" and password == "cc"):
            # Code to execute if the conditions are met
            

            # Add the logged-in user to UsersLoggedIn dictionary
            UsersLoggedIn[username] = TokenAccount(username, password)

            # Print all account instances
            for account_instance in TokenAccount.instances.values():
                #print(f"User :{account_instance.username}  Password:{account_instance.password}")

                loginUsr = f"Account {account_instance.username} is accessing to Login... +"
                print("+" * (len(loginUsr) + 3))
                print(f"+  {loginUsr}")

                print("+Logged in successfully!")
                print("+" * (len(loginUsr) + 3))
                print(f"Number of User Logged-in to the System : {len(UsersLoggedIn)}")
                print("+" * (len(loginUsr) + 3))

            #account_instance = UsersLoggedIn.get(username)
            #if account_instance:
            #    password = account_instance.password
            #    print(f"79=======: {username} {password}")
            #else:
            #    print("Account not found.")

            
            if UsersLoggedIn.get(username):
                password = UsersLoggedIn.get(username).password
                
                #print(f"User :{username} {password}")
                print(f"User :{username} STATUS: LOGGED IN")

            else:
                print("Account not found.")

            return True

        else:
            # Code to execute if the conditions are not met
            #print("Invalid username or password.")
            #return False
            
            error = "Username or password not provided."
            print(error)
            return False, str(error)


    except NameError:
        # Code to handle the case when the variables username or password are not defined
        error = "Username or password not provided."
        print(error)
        return False, str(error)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def login(username: str, password: str):
    device = {
        "device_type": "cisco_ios",
        "host": "sandbox-iosxr-1.cisco.com",
        "username": username,
        "password": password,
    }
    return validate_login(username, password, device, [])



def get_mapping_results(station):
    query = f"SELECT * FROM mapping WHERE station LIKE '%{station}%'"
    results = perform_search(query)
    return results


def get_vlan_results():
    query = f"SELECT * FROM vlans"
    results = perform_search(query)
    return results


def get_voice_results():
    query = f"SELECT * FROM voices"
    results = perform_search(query)
    return results









#===================================================================
@app.get("/")
async def home(request: Request):
    print("+++++++++++++++++++++++++++++++++++")
    print("+  User is preparing to Login...  +")
    print("+++++++++++++++++++++++++++++++++++")
    return templates.TemplateResponse("login.html", {"request": request})


#===================================================================
@app.post("/login")
async def process_login(
        request: Request, 
        username: str = Form(...), 
        password: str = Form(...)
        ):

    result = login(username, password)
    
    if result:
        return templates.TemplateResponse(
            "search.html", 
            {   "request": request, 
                "loginU_var": username
            }
        )
    else:
        return templates.TemplateResponse(
            "login.html", 
            {
                "request": request, 
                "error_message": error
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


    # Pass the results, search input, and loginU_var to the template
    if len(UsersLoggedIn) != 0:
        return templates.TemplateResponse(
            "search.html",
            {   "request": request, 
                "results": results, 
                "station": station, 
                "loginU_var": loginU_var,
                "resultsVLAN": resultsVLAN,
                "resultsVoice": resultsVoice  
            }
        )
    else:
        print("You must login first.")
        return templates.TemplateResponse("login.html", {"request": request})





#@app.post("/process_modal_form")
#===================================================================
@app.post("/process_modal_form1")
async def process_modal_form(
                request: Request, 
                loginU_var: str = Form(...),   
                idrow: str = Form(...),
                floor: str = Form(...),
                station: str = Form(...),                           
                port: str = Form(...), 
                interface: str = Form(...)
                ):
    

    print("==========================================================")
    print("Process: CLEAR PORT")
    print("-----------------")
    print("ID:", idrow)
    print("Station:", station)
    print("Port:", port)
    print("Interface:", interface)
    print("-----------------")
    print("Clear Port Performed by :", loginU_var)
    print("==========================================================")


    username = loginU_var
    account_instance = UsersLoggedIn.get(username)
    if account_instance:
        password = account_instance.password
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
                VLANCustom: str = Form(...)
                ):

    print("==========================================================")
    print("Process: Change VLAN")
    print("-----------------")
    print("ID:", idrow)
    print("Station:", station)
    print("Port:", port)
    print("Interface:", interface)
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
