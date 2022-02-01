from sqlalchemy.orm import Session

from pyd_models import AlertCreate
from orm_models import Alert, AlertStatus, LkpAlertStatus


def get_alert(db: Session, alert_nm: str):
    return db.query(Alert).filter(Alert.alert_nm == alert_nm).first()

def create_alert(db: Session, alert: AlertCreate):
    db_alert = Alert(alert_nm=alert.alert_nm)
    db.add(db_alert)
    db.commit()
    return db_alert

def create_alert_status(db: Session, alert: Alert):
    status = LkpAlertStatus.get_or_create(session=db, status_nm='silence')
    alert_status = AlertStatus(alert=alert, status=status)
    db.add(alert_status)
    db.commit()
    return alert_status