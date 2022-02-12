from pydantic import BaseModel


class AlertNm(BaseModel):
    alert_nm: str


class AlertBase(AlertNm):
    alert_desc: str
    
    class Config:
        orm_mode = True
        

class AlertCreate(AlertBase):
    pass
    

class AlertPyd(AlertBase):
    alert_id: int

