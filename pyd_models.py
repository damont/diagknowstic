from pydantic import BaseModel
from typing import Optional


class AlertNm(BaseModel):
    alert_nm: str


class AlertBase(AlertNm):
    alert_desc: str
    
    class Config:
        orm_mode = True
        

class AlertCreate(AlertBase):
    system_nm: Optional[str] = "default"
    
    
class AlertCreateOrm(AlertBase):
    system_id: int
    

class AlertPyd(AlertBase):
    alert_id: int
    
    
class SystemBase(BaseModel):
    system_nm: str
    system_desc: str
    
    class Config:
        orm_mode = True
    

class SystemPyd(SystemBase):
    system_id: int