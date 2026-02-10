from sqlalchemy.orm import Session
from models import Subscription
from datetime import datetime

def add_subscription(db: Session, name: str, amount: float, next_date_str: str):
    next_date = datetime.strptime(next_date_str, "%Y-%m-%d").date()
    subscription = Subscription(name=name, amount=amount, next_date=next_date)
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription

def get_subscriptions(db: Session):
    return db.query(Subscription).all()

def delete_subscription(db: Session, sub_id: int):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if sub:
        db.delete(sub)
        db.commit()
        return True
    return False
