from pydantic import BaseModel


class AlertBase(BaseModel):
    alert_nm: str
    alert_desc: str
    
    class Config:
        orm_mode = True
        

class AlertCreate(AlertBase):
    pass
    

class AlertPyd(AlertBase):
    alert_id: int

