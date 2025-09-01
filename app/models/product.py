from app.libraries import db
from datetime import date
from .associations import wishlist_products, product_categories
from .base import Entity

class Product(Entity):
    __tablename__ = 'products'
    
    name = db.Column(db.String(30), nullable=False, index=True)
    description = db.Column(db.String(180), nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    # N:M
    categories = db.relationship('Category', secondary=product_categories, back_populates='products', lazy='selectin')
    # N:1
    user_id = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    owner = db.relationship('User', back_populates='products')
    
    publish_date = db.Column(db.Date, nullable=False, default=date.today)
    fab_date = db.Column(db.Date, nullable=False)
    exp_date = db.Column(db.Date, nullable=False)
    
    wishlists = db.relationship('Wishlist', secondary=wishlist_products, back_populates='products',lazy='selectin')
    cart_items = db.relationship('CartItem', back_populates='product')
    stock_items = db.relationship('StockItem', back_populates='product')
    
    __table_args__ = (
        db.CheckConstraint('price >= 0', name='ck_product_price_nonneg'),
        db.CheckConstraint('exp_date > fab_date', name='ck_product_exp_after_fab'),
        db.CheckConstraint('exp_date > publish_date', name='ck_product_exp_after_publish')
    )