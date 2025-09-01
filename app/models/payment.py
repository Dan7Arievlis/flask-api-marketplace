from app.libraries import db
from .enums import PaymentStatusEnum, PaymentStatusType
from .base import Entity

class Payment(Entity):
    __tablename__ = 'payments'
    # N:1
    cart_id = db.Column(db.ForeignKey('carts.id', ondelete='CASCADE'), nullable=False, index=True)
    cart = db.relationship('Cart', back_populates='payments')
    
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    paid_at = db.Column(db.DateTime)
    status = db.Column(PaymentStatusType, nullable=False, default=PaymentStatusEnum.PENDING)
    
    provider = db.Column(db.String(30))
    external_id = db.Column(db.String(80))
    authorization_code = db.Column(db.String(40))

    __table_args__ = (
        db.CheckConstraint('amount > 0', name='ck_payment_amount_positive'),
        db.UniqueConstraint('provider', 'external_id', name='uq_payment_provider_extid')
    )

    
    def confirm(self):
        self.status = PaymentStatusEnum.CONFIRMED


    def fail(self):
        self.status = PaymentStatusEnum.FAILED
    