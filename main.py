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
    print(f"125 Perform Search")

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
            print("Logged in successfully!")

            # Add the logged-in user to UsersLoggedIn dictionary
            UsersLoggedIn[username] = TokenAccount(username, password)

            # Print all account instances
            for account_instance in TokenAccount.instances.values():
                print(f"line102=======: {account_instance.username} {account_instance.password}")

            print(f"length ====== {len(UsersLoggedIn)}")

            #account_instance = UsersLoggedIn.get(username)
            #if account_instance:
            #    password = account_instance.password
            #    print(f"79=======: {username} {password}")
            #else:
            #    print("Account not found.")

            
            if UsersLoggedIn.get(username):
                password = UsersLoggedIn.get(username).password
                print(f"line116=======: {username} {password}")
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


#===================================================================
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


#===================================================================
@app.post("/login")
async def process_login(request: Request, username: str = Form(...), password: str = Form(...)):
    print(f"107 LOGIN====== ")


    result = login(username, password)
    print(f"107 LOGIN Result======{result} ")

    if result:
        return templates.TemplateResponse("search.html", {"request": request, "loginU_var": username})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error_message": error})





#===================================================================
@app.post("/search")
async def search(request: Request, station: str = Form(...), loginU_var: str = Form(...)):
    # Connect to the SQLite database
    print(f"119 SEARCH====== {loginU_var}")

    #do query >> def perform_search(query):
    query = f"SELECT * FROM mapping WHERE station LIKE '%{station}%'"
    results = perform_search(query)


    query = f"SELECT * FROM vlans"
    resultsVLAN = perform_search(query)


    query = f"SELECT * FROM voices"
    resultsVoice = perform_search(query)

    # Pass the results and search input to the template
    print(f"length 131====== {len(UsersLoggedIn)}")


    # Pass the results, search input, and loginU_var to the template
    if len(UsersLoggedIn) != 0:
        return templates.TemplateResponse(
            "search.html",
            {"request": request, "results": results, "resultsVLAN": resultsVLAN, "resultsVoice": resultsVoice,"station": station, "loginU_var": loginU_var}
        )
    else:
        print("You must login first.")
        return templates.TemplateResponse("login.html", {"request": request})





#@app.post("/process_modal_form")
#===================================================================
@app.post("/process_modal_form1")
async def process_modal_form(request: Request, station: str = Form(...),port: str = Form(...), loginU_var: str = Form(...)):
    print("Modal 1 Pressed")
    print("Modal form submitted")

    print("Station:", station)
    print("Port:", port)
    print("Logged in as:", loginU_var)



    #do query >> def perform_search(query):
    query = f"SELECT * FROM mapping WHERE station LIKE '%{station}%'"
    results = perform_search(query)




    # Process the form data as needed
    
    username = loginU_var

    account_instance = UsersLoggedIn.get(username)
    if account_instance:
        password = account_instance.password
        print(f"180 Password is : {username} {password}")
    else:
        print("Account not found.")


    return templates.TemplateResponse(
        "search.html",
        {"request": request, "results": results,  "station": station, "loginU_var": loginU_var}

    )


#===================================================================
@app.post("/process_modal_form2")
async def process_modal_form(
                request: Request, 
                station: str = Form(...),
                port: str = Form(...), 
                interface: str = Form(...), 
                loginU_var: str = Form(...), 
                VlanCustom: str = Form(...)):

    print("Modal VLAN Pressed")
    print("Modal form submitted")
    print("Station:", station)
    print("Port:", port)
    print("Interface:", interface)
    print("Logged in as:", loginU_var)
    print("VLAN:", VlanCustom)
    



    username = loginU_var
    if UsersLoggedIn.get(username):
        password = UsersLoggedIn.get(username).password
        print(f"line116=======: {username} {password}")
    else:
        print("Account not found.")



    #do query >> def perform_search(query):
    query = f"SELECT * FROM mapping WHERE station LIKE '%{station}%'"
    results = perform_search(query)

    
    query = f"SELECT * FROM vlans"
    resultsVLAN = perform_search(query)

    # Process the form data as needed

    return templates.TemplateResponse(
        "search.html",
        {"request": request, "results": results, 
            "resultsVLAN": resultsVLAN, "station": station, "interface": interface,
            "loginU_var": loginU_var}

    )


#===================================================================
@app.post("/process_modal_form3")
async def process_modal_form(request: Request, 
                station: str = Form(...),
                port: str = Form(...), 
                loginU_var: str = Form(...), 
                VoiceCustom: str = Form(...)):

    print("Modal Voice Pressed")
    print("Modal form submitted")
    print("Station:", station)
    print("Port:", port)
    print("Logged in as:", loginU_var)
    print("Voice:", VoiceCustom)

    username = loginU_var
    if UsersLoggedIn.get(username):
        password = UsersLoggedIn.get(username).password
        print(f"line116=======: {username} {password}")
    else:
        print("Account not found.")

    #do query >> def perform_search(query):
    query = f"SELECT * FROM mapping WHERE station LIKE '%{station}%'"
    results = perform_search(query)

    
    query = f"SELECT * FROM voices"
    resultsVoice = perform_search(query)

    # Process the form data as needed

    return templates.TemplateResponse(
        "search.html",
        {"request": request, "results": results, "resultsVoice": resultsVoice, "station": station, "loginU_var": loginU_var}
    )




#===================================================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8886)

    #uvicorn.run(app, host="0.0.0.0", port=8886)
#   uvicorn main:app --reload --host 0.0.0.0 --port 8886
