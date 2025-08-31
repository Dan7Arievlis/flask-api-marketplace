from app.libraries import db
from .base import Entity

class Category(Entity):
    name = db.Column(db.String(20), nullable=False, unique=True, index=True)
    