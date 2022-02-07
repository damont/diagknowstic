# main.py

from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from pyd_models import AlertBase, AlertPyd
from orm_creates import get_alert, create_alert, create_alert_status, get_alert_page
from orm_actions import change_alert_status, get_all_alerts, get_alert_history
from alert_db import get_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def alerts(request: Request, db: Session = Depends(get_db)):
    alerts = get_all_alerts(db)
    return templates.TemplateResponse("alerts.html", context={
        "request": request,
        "alerts": alerts
    })


@app.get("/history")
def history(alert: str, request: Request, db: Session = Depends(get_db)):
    alerts = get_alert_history(db, alert)
    return templates.TemplateResponse("history.html", context={
        "request": request,
        "alerts": alerts
    }) 


@app.get("/alert")
def history(alert: str, request: Request, db: Session = Depends(get_db)):
    myalert = get_alert_page(db, alert)
    alerts = get_alert_history(db, alert, limit=3)
    return templates.TemplateResponse("alert.html", context={
        "request": request,
        "alert": myalert,
        "alerts": alerts
    })   


@app.post("/register", response_model=AlertPyd)
def register(alert : AlertBase, db: Session = Depends(get_db)):
    if get_alert(db, alert.alert_nm):
        raise HTTPException(status_code=400, 
                            detail=f'Already created {alert.alert_nm}')
    alert = create_alert(db, alert)
    create_alert_status(db, alert)
    return alert
    

@app.post("/alert")
def sound(alert : AlertBase, db: Session = Depends(get_db)):
    if not get_alert(db, alert.alert_nm):
        raise HTTPException(status_code=400, 
                            detail=f'No alert named {alert.alert_nm}')
    change_alert_status(db, alert.alert_nm, 'alert')


@app.post("/silence")
def silence(alert : AlertBase, db: Session = Depends(get_db)):
    if not get_alert(db, alert.alert_nm):
        raise HTTPException(status_code=400, 
                            detail=f'No alert named {alert.alert_nm}')
    change_alert_status(db, alert.alert_nm, 'silenced')
