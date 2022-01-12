# main.py

from fastapi import FastAPI

from pyd_models import AlertBase, Alert

app = FastAPI()

@app.post("/register", response_model=Alert)
async def register(alert : AlertBase):
    alert = Alert(alert_nm=alert.alert_nm, 
                  alert_id=1)
    return alert
    

@app.get("/sound/{alert_name}")
async def register():
    pass

@app.get("/silence/{alert_name}")
async def register():
    pass

@app.get("/status/{alert_name}")
async def register():
    pass