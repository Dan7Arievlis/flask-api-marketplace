from app.libraries import db
from .enums import ItemStatusType, ItemStatusEnum
from .base import Entity

class StockItem(Entity):
    __tablename__ = 'stock_items'
    
    # N:1
    stock_id = db.Column(db.ForeignKey('stocks.id', ondelete='CASCADE'), nullable=False, index=True)
    stock = db.relationship('Stock', back_populates='items')
    # N:1
    product_id = db.Column(db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False, index=True)
    product = db.relationship('Product', back_populates='stock_items')
    
    quantity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(ItemStatusType, nullable=False, default=ItemStatusEnum.OPEN)
    

    __table_args__ = (
        db.CheckConstraint('quantity >= 0', name='ck_stockitem_qty_nonneg'),
        db.UniqueConstraint('stock_id','product_id', name='uq_stockitem_unique_per_stock')
    )
    
    
    def set_quantity(self, quantity: int):
        self.quantity = quantity
    
    
    def set_status(self, status: str):
        try:
            self.status = ItemStatusEnum[status.lower()]
        except KeyError:
            self.status = ItemStatusEnum.OPEN
    
    