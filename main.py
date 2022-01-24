# main.py

from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from pyd_models import AlertBase, AlertPyd
from orm_creates import get_alert, create_alert, create_alert_status
from orm_actions import change_alert_status
from alert_db import get_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def alerts(request: Request):
    return templates.TemplateResponse("alerts.html", context={
        "request": request
    })


@app.post("/register", response_model=AlertPyd)
def register(alert : AlertBase, db: Session = Depends(get_db)):
    if get_alert(db, alert.alert_nm):
        raise HTTPException(status_code=400, 
                            detail=f'Already created {alert.alert_nm}')
    alert = create_alert(db, alert)
    create_alert_status(db, alert)
    return alert
    

@app.post("/sound")
def sound(alert : AlertBase, db: Session = Depends(get_db)):
    if not get_alert(db, alert.alert_nm):
        raise HTTPException(status_code=400, 
                            detail=f'No alert named {alert.alert_nm}')
    change_alert_status(db, alert.alert_nm, 'sound')


@app.post("/silence")
def silence(alert : AlertBase, db: Session = Depends(get_db)):
    if not get_alert(db, alert.alert_nm):
        raise HTTPException(status_code=400, 
                            detail=f'No alert named {alert.alert_nm}')
    change_alert_status(db, alert.alert_nm, 'silence')

@app.get("/status/{alert_name}")
async def register():
    pass