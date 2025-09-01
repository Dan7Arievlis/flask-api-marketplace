from enum import Enum
from app.libraries import db

class RolesEnum(str, Enum):
    ADMIN = 'admin'
    USER = 'user'


RolesType = db.Enem(RolesEnum, name='roles_enum', validate_strings=True)


class ItemStatusEnum(str, Enum):
    OPEN = 'open'
    ALLOCATED = 'allocated'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    RETURNED = 'returned'


ItemStatusType = db.Enum(ItemStatusEnum, name='item_status_enum', validate_strings=True)


class CartStatusEnum(str, Enum):
    OPEN = 'open'
    WAITING_PAYMENT = 'waiting_payment'
    PAID = 'paid' 
    CANCELED = 'canceled'


CartStatusType = db.Enum(ItemStatusEnum, name='item_status_enum', validate_strings=True)


class PaymentStatusEnum(str, Enum):
    PENDING = 'pending'
    AUTHORIZED = 'authorized'
    CONFIRMED = 'confirmed'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    CANCELED = 'canceled'


PaymentStatusType = db.Enum(PaymentStatusEnum, name='payment_status_enum', validate_strings=True)


class PaymentMethodEnum(str, Enum):
    PIX = 'pix'
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'
    BOLETO = 'boleto'


PaymentMethodType = db.Enum(PaymentMethodEnum, name='payment_method_enum', validate_strings=True)