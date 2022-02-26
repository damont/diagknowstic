from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from orm_models import Alert, AlertHistory, AlertStatus, LkpAlertStatus, System
from typing import Optional

def change_alert_status(db: Session, alert_nm: str, status: str):
    old_status = db.query(AlertStatus).\
        join(Alert, Alert.alert_id == AlertStatus.alert_id).\
        filter(Alert.alert_nm == alert_nm).first()
    
    history_record = AlertHistory.from_alert(old_status)
    db.add(history_record)
    
    old_status.status = LkpAlertStatus.get_or_create(session=db, status_nm=status)
    old_status.notes = ""
    
    db.commit()


def get_all_alerts(db: Session, system_nm: Optional[str] = None):
    all_alerts_q = db.query(Alert.alert_nm, 
                    LkpAlertStatus.status_nm,
                    LkpAlertStatus.status_color).\
        join(AlertStatus, AlertStatus.alert_id == Alert.alert_id).\
        join(LkpAlertStatus, LkpAlertStatus.status_id == AlertStatus.status_id)
        
    if system_nm:
        all_alerts_q = all_alerts_q.join(System, System.system_id == Alert.system_id).\
            filter(System.system_nm == system_nm)
            
    return all_alerts_q.all()
        
        
def get_systems(db: Session, system_nm: Optional[str] = None):
    
    # Get all of the alerts tied to a system and return the highest id across 
    # the alerts.
    session_status_sq = db.query(System.system_id,
                                 func.max(AlertStatus.status_id).label("max_status_id")).\
        join(Alert, Alert.system_id == System.system_id).\
        join(AlertStatus, AlertStatus.alert_id == Alert.alert_id)
        
    if system_nm:
        session_status_sq = session_status_sq.filter(System.system_nm == system_nm)
        
    session_status_sq = session_status_sq.group_by(System.system_id).subquery()
    
    all_q = db.query(System.system_nm,
                     System.system_desc,
                     func.coalesce(LkpAlertStatus.status_nm, "off").label("status_nm"),
                     func.coalesce(LkpAlertStatus.status_color, "grey").label("status_color")).\
        outerjoin(session_status_sq, session_status_sq.c.system_id == System.system_id).\
        outerjoin(LkpAlertStatus, LkpAlertStatus.status_id == session_status_sq.c.max_status_id)
        
    if system_nm:
        all_q = all_q.filter(System.system_nm == system_nm)
    
    return all_q.all()


def get_alert_history(db: Session, alert_nm: str, limit=1000):
    return db.query(LkpAlertStatus.status_nm,
                    LkpAlertStatus.status_color,
                    AlertHistory.post_time,
                    AlertHistory.notes,
                    Alert.alert_nm).\
        join(Alert, Alert.alert_id == AlertHistory.alert_id).\
        join(LkpAlertStatus, LkpAlertStatus.status_id == AlertHistory.status_id).\
        filter(Alert.alert_nm == alert_nm).\
        order_by(desc(AlertHistory.alert_history_id)).limit(limit)
        

def get_alert(db: Session, alert_nm: str):
    return Alert.get_or_create(session=db, alert_nm=alert_nm)


def update_alert_notes(db: Session, alert_id: int, alert_notes: str):
    db.query(AlertStatus).filter(AlertStatus.alert_id == alert_id).\
        update({AlertStatus.notes: alert_notes})
    db.commit()
