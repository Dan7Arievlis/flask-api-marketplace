from app.libraries import db
from .base import Entity

class Stock(Entity):
    name = db.Column(db.String(40), nullable=False, index=True)
    address = db.Column(db.String(200), nullable=False)
    # Many to one
    user_id = db.Column(db.Integer, nullable=False)
    # One to many
    # items = 
    