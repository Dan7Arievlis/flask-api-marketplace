from marshmallow import fields, validate, validates, ValidationError, post_load
from decimal import Decimal, ROUND_HALF_UP
from app.libraries import ma, db
from models.cart import Cart
from models.payment import Payment
from models.enums import PaymentMethodEnum, PaymentStatusEnum

class PaymentCreateSchema(ma.Schema):
    cart_id = fields.Int(
        required=True, 
        error_messages={
            'required': 'cart_id é obrigatório'
        })
    
    amount = fields.Decimal(
        required=True, 
        as_string=True, 
        places=2,
        validate=validate.Range(min=0.01, error='amount deve ser > 0')
        )
    
    method = fields.Enum(PaymentMethodEnum, by_value=True, required=True)
    paid_at = fields.DateTime(allow_none=True)

    provider = fields.Str(allow_none=True, validate=validate.Length(max=30))
    external_id = fields.Str(allow_none=True, validate=validate.Length(max=80))
    authorization_code = fields.Str(allow_none=True, validate=validate.Length(max=40))


    @validates('cart_id')
    def validate_cart(self, value, **kwargs):
        if not db.session.query(Cart.id).filter_by(id=value).first():
            raise ValidationError('Carrinho não encontrado.')


    @post_load
    def normalize(self, data, **kwargs):
        q = Decimal('0.01')
        data['amount'] = Decimal(str(data['amount'])).quantize(q, rounding=ROUND_HALF_UP)
        if 'provider' in data:
            self.context['provider'] = data['provider']
        return data


class PaymentResponseSchema(ma.Schema):
    id = fields.Int()
    cart_id = fields.Int()
    amount = fields.Decimal(as_string=True, places=2)
    method = fields.Enum(PaymentMethodEnum, by_value=True)
    provider = fields.Str(allow_none=True)
    external_id = fields.Str(allow_none=True)
    paid_at = fields.DateTime(allow_none=True)
    status = fields.Enum(PaymentStatusEnum, by_value=True)
    # authorization_code = fields.Str(allow_none=True)