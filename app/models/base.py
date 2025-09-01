from app.libraries import db
from datetime import datetime


class Entity(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now,nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    flg_active = db.Column(db.Boolean, default=True, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)
    
    
    def delete(self):
        self.deleted_at = datetime.now()
        self.flg_active = False
    
    
    def restore(self):
        self.deleted_at = None
        self.flg_active = True
    
    
    def set_updated_by(self, user):
        self.updated_by = user.id
    
    
    @property
    def is_deleted(self):
        return self.deleted_at is not None
    
    
    @property
    def is_active(self):
        return self.flg_active
