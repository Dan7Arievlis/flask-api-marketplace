from app.libraries import db
from datetime import datetime
from .enums import CartStatusEnum, CartStatusType
from .base import Entity

class Cart(Entity):
    __tablename__ = 'carts'
    
    # 1:1
    user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    user = db.relationship('User', back_populates='cart')
    # 1:N
    items = db.relationship('CartItem', back_populates='cart', cascade='all, delete-orphan', passive_deletes=True, lazy='selectin')
    
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    purchase_moment = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # 1:N
    payments = db.relationship('Payment', back_populates='cart', cascade='all, delete-orphan', passive_deletes=True, lazy='selectin')
    
    status = db.Column(CartStatusType, nullable=False, default=CartStatusEnum.OPEN)
    
    
    def set_status(self, status: str):
        try:
            self.status = CartStatusEnum[status.lower()]
        except KeyError:
            self.status = CartStatusEnum.OPEN
