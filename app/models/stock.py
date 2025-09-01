from app.libraries import db
from .base import Entity

class Stock(Entity):
    __tablename__ = 'stocks'
    
    name = db.Column(db.String(40), nullable=False, index=True)
    address = db.Column(db.String(200), nullable=False)
    # N:1
    user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User', back_populates='stocks')
    # 1:N
    items = db.relationship('StockItem', back_populates='stock', cascade='all, delete-orphan', passive_deletes=True, lazy='selectin', primaryjoin='Stock.id==StockItem.stock_id')

    def set_name(self, name: str):
        self.name = name