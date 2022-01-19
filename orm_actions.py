from sqlalchemy.orm import Session
from orm_models import Alert, AlertHistory, AlertStatus, LkpAlertStatus

def change_alert_status(db: Session, alert_nm: str, status: str):
    old_status = db.query(AlertStatus).\
        join(Alert, Alert.alert_id == AlertStatus.alert_id).\
        filter(Alert.alert_nm == alert_nm).first()
    
    history_record = AlertHistory.from_alert(old_status)
    db.add(history_record)
    
    old_status.status = LkpAlertStatus(status_nm=status)
    
    db.commit()