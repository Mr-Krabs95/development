from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/index.html")
def read_index(request:Request):
    return templates.TemplateResponse(request=request,
    name="index.html")

@app.get("/about.html")
def read_index(request:Request):
    return templates.TemplateResponse(request=request,
    name="about.html")

@app.get("/form_data.html")
def read_index(request:Request):
    return templates.TemplateResponse(request=request,
    name="form_data.html")