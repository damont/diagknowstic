from sqlalchemy.sql.expression import null
from alert_db import Base, engine
from sqlalchemy import Integer, Text, Column, DateTime


class Alert(Base):
    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    alert_nm = Column(Text, nullable=False)


class LkpAlertStatus(Base):
    status_id = Column(Integer, primary_key=True)
    status_nm = Column(Text)


class AlertStatus(Base):
    alert_status_id = Column(Integer, primary_key=True)
    alert_id = Column(Integer)
    status_id = Column(Integer)
    
     
class AlertHistory(Base):
    alert_history_id = Column(Integer, primary_key=True)
    alert_id = Column(Integer)
    tatus_id = Column(Integer)

    
def init_db():
    Base.metadata.create_all(engine)