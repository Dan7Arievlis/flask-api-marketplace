from app.libraries import db
from .enums import ItemStatusType, ItemStatusEnum
from .base import Entity

class CartItem(Entity):
    __tablename__ = 'cart_items'
    
    # N:1
    cart_id = db.Column(db.ForeignKey('carts.id', ondelete='CASCADE'), nullable=False, index=True)
    cart = db.relationship('Cart', back_populates='items')
    # N:1
    product_id = db.Column(db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False, index=True)
    product = db.relationship('Product', back_populates='cart_items')
    
    quantity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(ItemStatusType, nullable=False, default=ItemStatusEnum.OPEN)
    
    __table_args__ = (
        db.CheckConstraint('quantity > 0', name='ck_cartitem_qty_positive'),
        db.UniqueConstraint('cart_id', 'product_id', name='uq_unique_product_per_cart')
    )
    
    
    def set_quantity(self, quantity: int):
        self.quantity = quantity
    
    
    def set_status(self, status: str):
        try:
            self.status = ItemStatusEnum[status.lower()]
        except KeyError:
            self.status = ItemStatusEnum.OPEN
