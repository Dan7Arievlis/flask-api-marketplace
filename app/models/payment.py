from app.libraries import db
from datetime import datetime
from .base import Entity

class Payment(Entity):
    cart_id = db.Column(db.Integer, nullable=False)
    moment = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    