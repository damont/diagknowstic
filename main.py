# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from pyd_models import AlertBase, AlertPyd
from orm_creates import get_alert, create_alert
from alert_db import get_db

app = FastAPI()

@app.post("/register", response_model=AlertPyd)
async def register(alert : AlertBase, db: Session = Depends(get_db)):
    if get_alert(db, alert.alert_nm):
        raise HTTPException(status_code=400, 
                            detail=f'Already created {alert.alert_nm}')
    return create_alert(db, alert)
    

@app.get("/sound/{alert_name}")
async def register():
    pass

@app.get("/silence/{alert_name}")
async def register():
    pass

@app.get("/status/{alert_name}")
async def register():
    pass