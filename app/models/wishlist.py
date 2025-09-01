from app.libraries import db
from .associations import wishlist_products
from .base import Entity

class Wishlist(Entity):
    __tablename__ = 'wishlists'
    
    # 1:1
    user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    user = db.relationship('User', back_populates='wishlist')
    # N:M
    products = db.relationship('Product', secondary=wishlist_products, back_populates='wishlists', lazy='selectin')