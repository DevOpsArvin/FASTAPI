from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

login_var = ""

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Connect to the SQLite database
conn = sqlite3.connect("epmap.db")
cursor = conn.cursor()


def validate_login(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output

        print("Login Successfull - Proceed to Search")
        return True

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
        return False



def login(username: str, password: str):
    device = {
        "device_type": "cisco_ios",
        "host": "sandbox-iosxr-1.cisco.com",
        "username": username,
        "password": password,
    }
    return validate_login(device, [])
    


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def process_login(request: Request, username: str = Form(...), password: str = Form(...)):

    result = login(username, password)
    print(result)
    print(username)
    print(password)
   
    if result:
        print("go Search")
        global login_var
        login_var = username
        print("74 ",login_var)
        
        return templates.TemplateResponse("search.html", {"request": request})
    else:
        return templates.TemplateResponse("login.html", {"request": request})

@app.post("/search")
def search(request: Request, station: str = Form(...)):
    # Connect to the SQLite database
    conn = sqlite3.connect("epmap.db")
    cursor = conn.cursor()

    # Perform the search query
    query = f"SELECT * FROM mapping WHERE station LIKE '%{station}%'"
    cursor.execute(query)
    results = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Pass the results and search input to the template
    print("96 ",login_var)
    if login_var != "":
        
        return templates.TemplateResponse(
            "search.html",
            {"request": request, "results": results, "station": station}
        )

    else:
        return templates.TemplateResponse("login.html", {"request": request})





@app.get("/search")
def search(request: Request):
    print("get Search")
    print("107 ",login_var) 
    if login_var != "":
        return templates.TemplateResponse("search.html", {"request": request})
    else:
        return templates.TemplateResponse("login.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
