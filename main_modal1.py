from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("modal1.html", {"request": request})


@app.post('/process-modal1')
def process_modal1():
    print("Task done  1 !")
    return {"message": "Task completed successfully."}


@app.post('/process-modal2')
def process_modal2():
    print("Task done  2 !")
    return {"message": "Task completed successfully."}





if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
