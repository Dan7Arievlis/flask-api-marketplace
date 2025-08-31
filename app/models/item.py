from app.libraries import db
from .base import Entity

class Item(Entity):
    # Many to one
    collection_id = db.Column(db.Integer, nullable=False)
    # Many to one
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.Enum('open', 'allocated', 'shipped', 'delivered', 'returned'), nullable=False, default='open')
    
    
    def set_quantity(self, quantity: int):
        self.quantity = quantity
    
    
    def set_status(self, status: str):
        valid_status = ['open', 'allocated', 'shipped', 'delivered', 'returned']
        if status.lower() in valid_status:
            self.status = status.lower()
            return
        
        self.status = 'open'
    
    