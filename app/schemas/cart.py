from marshmallow import fields, validate, validates, post_load
from models.enums import CartStatusEnum
from app.libraries import ma

class CartUpdateSchema(ma.Schema):
    status = fields.Enum(
        CartStatusEnum,
        by_value=True,
        allow_none=True,
        load_default=getattr(CartStatusEnum, 'OPEN', 'open'),
        error_messages={
            'invalid': 'Role deve pertencer ao enum CartItemStatus'
        })
    
    purchase_moment = fields.DateTime(allow_none=True)


class CartResponseSchema(ma.Schema):
    id = fields.Int()
    user_id = fields.Int()
    total = fields.Decimal(as_string=True, places=2)
    purchase_moment = fields.DateTime()
    status = fields.Enum(CartStatusEnum, by_value=True)