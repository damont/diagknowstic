from sqlalchemy.orm import Session
from sqlalchemy import desc
from orm_models import Alert, AlertHistory, AlertStatus, LkpAlertStatus

def change_alert_status(db: Session, alert_nm: str, status: str):
    old_status = db.query(AlertStatus).\
        join(Alert, Alert.alert_id == AlertStatus.alert_id).\
        filter(Alert.alert_nm == alert_nm).first()
    
    history_record = AlertHistory.from_alert(old_status)
    db.add(history_record)
    
    old_status.status = LkpAlertStatus.get_or_create(session=db, status_nm=status)
    
    db.commit()


def get_all_alerts(db: Session):
    return db.query(Alert.alert_nm, 
                    LkpAlertStatus.status_nm,
                    LkpAlertStatus.status_color).\
        join(AlertStatus, AlertStatus.alert_id == Alert.alert_id).\
        join(LkpAlertStatus, LkpAlertStatus.status_id == AlertStatus.status_id).\
        all()


def get_alert_history(db: Session, alert_nm: str, limit=1000):
    return db.query(AlertHistory.status_id,
                    AlertHistory.post_time,
                    Alert.alert_nm).\
        join(Alert, Alert.alert_id == AlertHistory.alert_id).\
        filter(Alert.alert_nm == alert_nm).\
        order_by(desc(AlertHistory.alert_history_id)).limit(limit)
        

def get_alert(db: Session, alert_nm: str):
    return Alert.get_or_create(session=db, alert_nm=alert_nm)
