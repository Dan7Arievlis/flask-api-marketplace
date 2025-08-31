from app.libraries import db
from .base import Entity

class WishList(Entity):
    # One to one
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    # One to many
    # products = 