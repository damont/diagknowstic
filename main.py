# main.py

from fastapi import FastAPI, Depends, HTTPException, Request, Form
from typing import Optional
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from pyd_models import AlertPyd, AlertNm, SystemPyd, SystemBase, AlertCreate, AlertCreateOrm
from orm_creates import get_alert, create_alert, create_alert_status, get_alert_page, get_system, create_system
from orm_actions import change_alert_status, get_all_alerts, get_alert_history, update_alert_notes, get_systems
from alert_db import get_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")


"""
The first section of routes are devoted to the UI.
"""

@app.get("/")
def systems(request: Request, db: Session = Depends(get_db)):
    systems = get_systems(db)
    return templates.TemplateResponse("systems.html", context={
        "request": request,
        "systems": systems
    })
    
    
@app.get("/systempage")
def systempage(system: str, request: Request, db: Session = Depends(get_db)):
    alerts = get_all_alerts(db, system)
    system_info = get_systems(db, system)
    
    if system_info:
        system_info = system_info[0]
    else:
        raise HTTPException(status_code=400, 
                            detail=f'Requested System does not exist {system}')
    
    return templates.TemplateResponse("system.html", context={
        "request": request,
        "alerts": alerts,
        "system": system_info
    })


@app.get("/alertpage")
def alertpage(alert: str, request: Request, db: Session = Depends(get_db)):
    myalert = get_alert_page(db, alert)
    alerts = get_alert_history(db, alert, limit=3)
    return templates.TemplateResponse("alert.html", context={
        "request": request,
        "alert": myalert,
        "alerts": alerts
    })  


@app.post("/alertpage")
def alertpage(alert: str, 
              request: Request, 
              alert_notes: Optional[str] = Form(None), 
              new_status: Optional[str] = Form(None), 
              db: Session = Depends(get_db)):
    alert_for_id = get_alert(db, alert)
    if alert_notes:
        update_alert_notes(db, alert_for_id.alert_id, alert_notes)
    if new_status:
        change_alert_status(db, alert, new_status)
    # TODO: This seems like a hacky way to return to the alertpage get route.
    redirect_url = request.url_for('alertpage') + f'?alert={alert}'
    return RedirectResponse(redirect_url, status_code=303)


@app.get("/history")
def history(alert: str, request: Request, db: Session = Depends(get_db)):
    alerts = get_alert_history(db, alert)
    return templates.TemplateResponse("history.html", context={
        "request": request,
        "alerts": alerts,
        "alert": alert
    }) 


"""
API section for registering alerts and interacting with those alerts!
"""


@app.post("/register/alert", response_model=AlertPyd)
def register_alert(alert : AlertCreate, db: Session = Depends(get_db)):
    if get_alert(db, alert.alert_nm):
        raise HTTPException(status_code=400, 
                            detail=f'Already created {alert.alert_nm}')
        
    # Alerts are created with system names, but the alert table only has system ID
    # so let's get the system first.
    system = get_system(db, system_nm=alert.system_nm)
    if not system:
        raise HTTPException(status_code=400, 
                            detail=f'Cannot add alert to system {alert.system_nm} as system does not exist')
        
    # Now we need to pass the AlertCreate but remove the system_nm and add the system_id.
    new_alert = AlertCreateOrm(alert_nm=alert.alert_nm,
                               alert_desc=alert.alert_desc,
                               system_id=system.system_id)
                
    alert = create_alert(db, new_alert)
    create_alert_status(db, alert)
    return alert


@app.post("/register/system", response_model=SystemPyd)
def register_system(system : SystemBase, db: Session = Depends(get_db)):
    if get_system(db, system.system_nm):
        raise HTTPException(status_code=400, 
                            detail=f'Already created {system.system_nm}')
    system = create_system(db, system)
    return system
    

@app.post("/alert")
def alert(alert : AlertNm, db: Session = Depends(get_db)):
    if not get_alert(db, alert.alert_nm):
        raise HTTPException(status_code=400, 
                            detail=f'No alert named {alert.alert_nm}')
    change_alert_status(db, alert.alert_nm, 'alert')


@app.post("/silence")
def silence(alert : AlertNm, db: Session = Depends(get_db)):
    if not get_alert(db, alert.alert_nm):
        raise HTTPException(status_code=400, 
                            detail=f'No alert named {alert.alert_nm}')
    change_alert_status(db, alert.alert_nm, 'silence')


@app.post("/nominal")
def nominal(alert : AlertNm, db: Session = Depends(get_db)):
    if not get_alert(db, alert.alert_nm):
        raise HTTPException(status_code=400, 
                            detail=f'No alert named {alert.alert_nm}')
    change_alert_status(db, alert.alert_nm, 'nominal')
