from marshmallow import fields, validate, validates, post_load, ValidationError
from .product import ProductResponseSchema
from models.enums import ItemStatusEnum
from models.product import Product
from app.libraries import ma, db

class StockItemCreateSchema(ma.Schema):
    product_id = fields.Int(
        required=True, 
        error_messages={
            'required': 'Id do produto é obrigatório'
        })
    
    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            'required': 'Campo de quantidade é obrigatório'
        })


    @validates("product_id")
    def validate_product_exists(self, value, **kwargs):
        if not db.session.query(Product.id).filter_by(id=value).first():
            raise ValidationError("Produto não encontrado.")


class StockItemUpdateSchema(ma.Schema):
    quantity = fields.Int(allow_none=True, validate=validate.Range(min=1))
    status = fields.Enum(ItemStatusEnum, by_value=True, allow_none=True)


class StockItemResponseSchema(ma.Schema):
    id = fields.Int()
    stock_id = fields.Int()
    product_id = fields.Int()
    quantity = fields.Int()
    item_status = fields.Enum(ItemStatusEnum, by_value=True, attribute="status")
    product = fields.Nested(ProductResponseSchema)