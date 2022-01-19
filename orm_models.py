from sqlalchemy.sql.expression import null
from alert_db import Base, engine
from sqlalchemy import Integer, Text, Column, ForeignKey
from sqlalchemy.orm import relationship


class Alert(Base):
    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    alert_nm = Column(Text, nullable=False)


class LkpAlertStatus(Base):
    status_id = Column(Integer, primary_key=True)
    status_nm = Column(Text)


class AlertStatus(Base):
    alert_status_id = Column(Integer, primary_key=True)
    alert_id = Column(Integer, ForeignKey(Alert.alert_id))
    status_id = Column(Integer, ForeignKey(LkpAlertStatus.status_id))
    
    alert = relationship("Alert")
    status = relationship("LkpAlertStatus")
    
     
class AlertHistory(Base):
    alert_history_id = Column(Integer, primary_key=True)
    alert_id = Column(Integer)
    status_id = Column(Integer)
    
    alert_id = Column(Integer, ForeignKey(Alert.alert_id))
    status_id = Column(Integer, ForeignKey(LkpAlertStatus.status_id))
    
    @classmethod
    def from_alert(cls, alert: AlertStatus):
        return AlertHistory(alert_id=alert.alert_id, status_id=alert.status_id)

    
def init_db():
    Base.metadata.create_all(engine)