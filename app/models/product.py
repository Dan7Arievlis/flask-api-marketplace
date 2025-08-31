from app.libraries import db
from datetime import date
from .base import Entity

class Product(Entity):
    name = db.Column(db.String(30), nullable=False, index=True)
    description = db.Column(db.String(180), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    # Many to one
    # category_id = 
    # Many to one
    # vendor_id = 
    publish_date = db.Column(db.Date, nullable=False, default=date.today())
    fab_date = db.Column(db.Date, nullable=False)
    exp_date = db.Column(db.Date, nullable=False)
    