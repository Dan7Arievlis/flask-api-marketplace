from app.libraries import db
from datetime import datetime
from .base import Entity

class Cart(Entity):
    # One to one
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    # One to many
    # items = 
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    purchase_moment = db.Column(db.Timestemp, nullable=False, default=datetime.now())
    # One to many
    # payments = 
    status = db.Column(db.Enum('open', 'waiting_payment', 'paid', 'canceled'), nullable=False, default='open')
    
    
    def set_status(self, status: str):
        valid_status = ['open', 'waiting_payment', 'paid', 'canceled']
        if status.lower() in valid_status:
            self.status = status.lower()
            return
        
        self.status = 'open'
