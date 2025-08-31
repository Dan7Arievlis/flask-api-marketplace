from app.libraries import db
from .base import Entity
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash


class User(Entity):
    username = db.Column(db.String(30), nullable=False, unique=True, index=True)
    email = db.Column(db.String(80), nullable=False, unique=True, index=True)
    password = db.Column(db.String(400), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    balance = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    address = db.Column(db.String(200))
    telephone = db.Column(db.String(15))
    role = db.Column(db.Enum('admin', 'user'), nullable=False, default='user')
    
    # One to one
    # wishlist = 
    # One to Many
    # stocks = 
    # One to one
    # cart = 

    def set_password(self, password):
        self.password = generate_password_hash(password)


    def set_balance(self, amount):
        self.balance = amount
    
    
    def set_address(self, address: str):
        self.address = address
    
    
    def set_telephone(self, telephone: str):
        self.telephone = telephone
    
    
    def set_role(self, role: str):
        valid_roles = ['admin', 'user']
        if role.lower() in valid_roles:
            self.role = role.lower()
            return
        
        self.role = 'user'
    
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    
    @property
    def age(self):
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) \
            < (self.birth_date.month, self.birth_date.day))

        return age