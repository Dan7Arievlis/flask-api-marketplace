from app.libraries import db
from .base import Entity
from .enums import RolesEnum, RolesType
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash


class User(Entity):
    __tablename__ = 'users'
    
    username = db.Column(db.String(30), nullable=False, unique=True, index=True)
    email = db.Column(db.String(130), nullable=False, unique=True, index=True)
    password = db.Column(db.String(400), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    balance = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(15))
    role = db.Column(RolesType, nullable=False, default=RolesEnum.USER)
    # 1:1
    wishlist = db.relationship('Wishlist', back_populates='user', uselist=False, cascade='all, delete-orphan', passive_deletes=True, lazy='selectin')
    # 1:N
    stocks = db.relationship('Stock', back_populates='user', cascade='all, delete-orphan', passive_deletes=True, lazy='selectin', primaryjoin='User.id==Stock.user_id')
    # 1:1
    cart = db.relationship('Cart', back_populates='user', uselist=False, cascade='all, delete-orphan', passive_deletes=True, lazy='selectin')
    # 1:N
    products = db.relationship('Product', back_populates='owner', cascade='all, delete-orphan', passive_deletes=True, single_parent=True, lazy='selectin')


    def set_password(self, password):
        self.password = generate_password_hash(password)


    def set_balance(self, amount):
        self.balance = amount
    
    
    def set_address(self, address: str):
        self.address = address
    
    
    def set_phone(self, phone: str):
        self.phone = phone
    
    
    def set_role(self, role: str):
        try:
            self.role = RolesEnum[role.lower()]
        except KeyError:
            self.role = RolesEnum.USER
    
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    
    @property
    def is_admin(self):
        return self.role == RolesEnum.ADMIN
    
    
    @property
    def age(self):
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) \
            < (self.birth_date.month, self.birth_date.day))

        return age