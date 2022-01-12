from sqlalchemy.orm import Session

from pyd_models import AlertCreate
from orm_models import Alert


def get_alert(db: Session, alert_nm: str):
    return db.query(Alert).filter(Alert.alert_nm == alert_nm).first()

def create_alert(db: Session, alert: AlertCreate):
    db_alert = Alert(alert_nm=alert.alert_nm)
    db.add(db_alert)
    db.commit()
    return db_alert