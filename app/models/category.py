from app.libraries import db
from .associations import product_categories
from .base import Entity

class Category(Entity):
    __tablename__ = 'categories'
    
    # M:N
    products = db.relationship('Product', secondary=product_categories, back_populates='categories', lazy='selectin')
    name = db.Column(db.String(20), nullable=False, unique=True, index=True)
