from alert_db import engine as prod_engine, get_db
from sqlalchemy import Integer, Text, Column, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr
import re


def _cc2jl(string):
    REGEX = r'(.(?:[^a-z_]+(?=[A-Z_]|$)|[^A-Z_]+))'
    def _jl_match(match):
        group = match.group()
        prefix = bool(match.start() and not group.startswith('_'))
        return '_' * prefix + group.lower()

    return re.subn(REGEX, _jl_match, string)[0]


class SABase(object):
    
    @declared_attr
    def __tablename__(cls):
        return _cc2jl(cls.__name__)

    @classmethod
    def get_or_create(cls, session, **kwargs):
        instance = session.query(cls).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = cls(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    post_time = Column(DateTime, server_default=func.now())
    

Base = declarative_base(cls=SABase)


class System(Base):
    system_id = Column(Integer, primary_key=True, autoincrement=True)
    system_nm = Column(Text, nullable=False, unique=True)
    system_desc = Column(Text, nullable=False) 


class Alert(Base):
    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    alert_nm = Column(Text, nullable=False, unique=True)
    alert_desc = Column(Text, nullable=False)
    system_id = Column(Integer, ForeignKey(System.system_id), nullable=False)
    
    system = relationship("System")


class LkpAlertStatus(Base):
    status_id = Column(Integer, primary_key=True)
    status_nm = Column(Text, nullable=False, unique=True)
    status_color = Column(Text, nullable=False, default='grey')


class AlertStatus(Base):
    alert_status_id = Column(Integer, primary_key=True)
    alert_id = Column(Integer, ForeignKey(Alert.alert_id), nullable=False)
    status_id = Column(Integer, ForeignKey(LkpAlertStatus.status_id), nullable=False)
    notes = Column(Text, nullable=False, default='')
    
    alert = relationship("Alert")
    status = relationship("LkpAlertStatus")
    
     
class AlertHistory(Base):
    alert_history_id = Column(Integer, primary_key=True)
    alert_id = Column(Integer)
    status_id = Column(Integer)
    notes = Column(Text)
    
    alert_id = Column(Integer, ForeignKey(Alert.alert_id))
    status_id = Column(Integer, ForeignKey(LkpAlertStatus.status_id))
    
    @classmethod
    def from_alert(cls, alert: AlertStatus):
        return AlertHistory(alert_id=alert.alert_id, 
                            status_id=alert.status_id,
                            notes=alert.notes)

    
def init_db(engine=None, db_func=get_db):
    if not engine:
        engine = prod_engine
    Base.metadata.create_all(engine)

    # Hacky way to get database session from get_db function.
    for session in db_func():
        session.add(LkpAlertStatus(status_nm='off', status_color='grey'))
        session.add(LkpAlertStatus(status_nm='nominal', status_color='green'))
        session.add(LkpAlertStatus(status_nm='silence', status_color='orange'))
        session.add(LkpAlertStatus(status_nm='alert', status_color='red'))
        session.commit()
        
        system = System(system_nm="default", system_desc="Don't use this bucket")
        session.add(system)
        session.commit()

        alert = Alert(alert_nm='fake', alert_desc='Is everything OK?')
        alert_status = AlertStatus()
        alert_status.alert = alert
        alert_status.status = LkpAlertStatus.get_or_create(session, status_nm='off')
        alert.system = system

        session.add(alert_status)
        session.commit()