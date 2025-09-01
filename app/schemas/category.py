from marshmallow import fields, validate, post_load
from app.libraries import ma


class CategoryCreateSchema(ma.Schema):
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=2, max=20), 
        error_messages={
            'required': 'Nome é um campo obrigatório',
            'invalid': 'Nome deve ser uma string válida'
        })


    @post_load
    def normalize(self, data, **kwargs):
        data['name'] = data['name'].strip().lower()
        return data


class CategoryUpdateSchema(ma.Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=20), 
        error_messages={
            'required': 'Nome é um campo obrigatório',
            'invalid': 'Nome deve ser uma string válida'
        })


    @post_load
    def normalize(self, data, **kwargs):
        data['name'] = data['name'].strip().lower()
        return data


class CategoryResponseSchema(ma.Schema):
    id = fields.Int()
    name = fields.Str()