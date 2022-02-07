from sqlalchemy.orm import Session

from pyd_models import AlertCreate
from orm_models import Alert, AlertStatus, LkpAlertStatus


def get_alert(db: Session, alert_nm: str):
    return db.query(Alert).filter(Alert.alert_nm == alert_nm).first()

def create_alert(db: Session, alert: AlertCreate):
    return Alert.get_or_create(session=db, **alert.dict())

def create_alert_status(db: Session, alert: Alert):
    status = LkpAlertStatus.get_or_create(session=db, status_nm='silence')
    alert_status = AlertStatus(alert=alert, status=status)
    db.add(alert_status)
    db.commit()
    return alert_status

def get_alert_page(db: Session, alert_nm: str):
    return db.query(Alert.alert_nm, 
                    Alert.alert_desc,
                    LkpAlertStatus.status_nm,
                    LkpAlertStatus.status_color).\
        join(AlertStatus, AlertStatus.alert_id == Alert.alert_id).\
        join(LkpAlertStatus, LkpAlertStatus.status_id == AlertStatus.status_id).\
        filter(Alert.alert_nm == alert_nm).first()