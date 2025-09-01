from marshmallow import fields, validate, validates, post_load, ValidationError
from models.user import User
from models.enums import ItemStatusEnum
from app.libraries import ma, db

class StockCreateSchema(ma.Schema):
    user_id = fields.Int(load_only=True, allow_none=True)
    
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=40),
        error_messages={
            'required': 'Nome é obrigatório',
            'invalid': 'Nome deve ser uma string válida'
        })
    
    address = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=200),
        error_messages={
            'required': 'Endereço é obrigatório',
            'invalid': 'Endereço deve ser uma string válida'
        })


    @validates('user_id')
    def validate_user(self, value, **kwargs):
        if value is None:
            return
        exists = db.session.query(User.id).filter_by(id=value).first()
        if not exists:
            raise ValidationError('Usuário (user_id) não encontrado.')


    @post_load
    def normalize(self, data, **kwargs):
        data['name'] = data['name'].strip().title()
        data['address'] = data['address'].strip()
        return data


class StockUpdateSchema(ma.Schema):
    name = fields.Str(allow_none=True, validate=validate.Length(min=2, max=40))
    address = fields.Str(allow_none=True, validate=validate.Length(min=3, max=200))


    @post_load
    def normalize(self, data, **kwargs):
        if data.get('name') is not None:
            data['name'] = data['name'].strip().title()
        if data.get('address') is not None:
            data['address'] = data['address'].strip()
        return data


class StockResponseSchema(ma.Schema):
    id = fields.Int()
    name = fields.Str()
    address = fields.Str()
    user_id = fields.Int()