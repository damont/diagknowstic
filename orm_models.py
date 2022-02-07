from sqlalchemy.sql.expression import null
from alert_db import Base, engine, get_db
from sqlalchemy import Integer, Text, Column, ForeignKey
from sqlalchemy.orm import relationship


class Alert(Base):
    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    alert_nm = Column(Text, nullable=False, unique=True)
    alert_desc = Column(Text, nullable=False)


class LkpAlertStatus(Base):
    status_id = Column(Integer, primary_key=True)
    status_nm = Column(Text, nullable=False, unique=True)
    status_color = Column(Text, nullable=False, default='grey')


class AlertStatus(Base):
    alert_status_id = Column(Integer, primary_key=True)
    alert_id = Column(Integer, ForeignKey(Alert.alert_id), nullable=False)
    status_id = Column(Integer, ForeignKey(LkpAlertStatus.status_id), nullable=False)
    
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

    # Hacky way to get database session from get_db function.
    for session in get_db():
        session.add(LkpAlertStatus(status_nm='nominal', status_color='green'))
        session.add(LkpAlertStatus(status_nm='alert', status_color='red'))
        session.add(LkpAlertStatus(status_nm='silenced', status_color='orange'))
        session.add(LkpAlertStatus(status_nm='off', status_color='grey'))
        session.commit()