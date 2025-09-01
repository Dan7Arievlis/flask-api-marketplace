from marshmallow import fields, validate, validates, ValidationError
from models.product import Product
from models.associations import wishlist_products
from app.libraries import ma, db

class ProductMiniSchema(ma.Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Decimal(as_string=True, places=2)


class WishlistResponseSchema(ma.Schema):
    id = fields.Int()
    user_id = fields.Int()
    products = fields.List(fields.Nested(ProductMiniSchema))


class WishlistAddProductSchema(ma.Schema):
    product_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            'required': 'Id do produto é obrigatório'
        })


    @validates("product_id")
    def validate_product(self, value, **kwargs):
        if not db.session.query(Product.id).filter_by(id=value).first():
            raise ValidationError("Produto não encontrado.")

        wishlist_id = self.context.get("wishlist_id")
        if wishlist_id:
            exists = db.session.execute(
                wishlist_products.select().where(
                    wishlist_products.c.wishlist_id == wishlist_id,
                    wishlist_products.c.product_id == value
                )
            ).first()
            if exists:
                raise ValidationError("Produto já está na wishlist.")


class WishlistRemoveProductSchema(ma.Schema):
    product_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            'required': 'product_id é obrigatório'
        })