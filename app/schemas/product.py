from marshmallow import fields, validate, validates, ValidationError, post_load, validates_schema, post_dump
from app.libraries import ma, db
from decimal import Decimal, ROUND_HALF_UP
# from models.enums import RolesEnum
from models.user import User
from models.category import Category
import re
from datetime import date


class ProductCreateSchema(ma.Schema):
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=30), 
        error_messages={
            'required': 'Nome é um campo obrigatório',
            'invalid': 'Nome deve ser uma string válida'
        })
    
    description = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=180),
        error_messages={
            'required': 'Descrição é um campo obrigatório',
            'invalid': 'Descrição deve ser uma string válida'
        }
    )

    categories = fields.List(
        fields.Str(),
        required=True,
        validate=validate.Length(min=1),
        error_messages={'required': 'Informe pelo menos uma categoria'}
    )

    price = fields.Decimal(
        required=True,
        as_string=True,
        places=2,
        validate=validate.Range(min=0, error='Preço deve ser maior ou igual a 0')
    )

    owner_id = fields.Integer(
        required=True,
        error_messages={'required': 'owner_id é obrigatório'}
    )

    publish_date = fields.Date(load_default=date.today)
    fab_date     = fields.Date(allow_none=True)
    exp_date     = fields.Date(allow_none=True)


    @validates('owner_id')
    def validate_owner(self, value: int):
        if not db.session.query(User.id).filter_by(id=value).first():
            raise ValidationError('Usuário (owner_id) não encontrado.')


    @validates('categories')
    def validate_categories(self, value: list[str]):
        names = [v.strip() for v in value if isinstance(v, str) and v.strip()]
        if not names:
            raise ValidationError('Informe ao menos uma categoria válida.')

        rows = Category.query.filter(Category.name.in_(names)).all()
        found = {c.name for c in rows}
        missing = [n for n in names if n not in found]
        if missing:
            raise ValidationError(f'Categorias inexistentes: {", ".join(missing)}')
        self.context['__resolved_categories__'] = rows

    
    @validates_schema
    def validate_dates(self, data, **kwargs):
        pub = data.get('publish_date') or date.today()
        fab = data.get('fab_date')
        exp = data.get('exp_date')
        
        perishables = {'comida', 'perecivel'}
        
        cat_names = data.get('categories') or []
        normalized = {normalized(x) for x in cat_names if isinstance(x, str)}
        require_perishable = any(x in perishables for x in normalized)

        if require_perishable:
            errs = {}
            if fab is None:
                errs['fab_date'] = ['Data de fabricação é obrigatória para produtos perecíveis.']
            if exp is None:
                errs['exp_date'] = ['Data de validade é obrigatória para produtos perecíveis.']
            if errs:
                raise ValidationError(errs)

        if fab and exp and not (fab < exp):
            raise ValidationError({'exp_date': 'Data de validade deve ser maior que data de fabricação.'})
        if exp and pub and not (exp > pub):
            raise ValidationError({'exp_date': 'Data de validade deve ser maior que data de publicação.'})

    
    @post_load
    def normalize_data(self, data, **kwargs):
        data['name'] = data['name'].strip().lower()
        data['description'] = data['description'].strip().lower()
        data['user_id'] = data.pop('owner_id')
        
        if '__resolved_categories__' in self.context:
            data['categories'] = self.context.pop('__resolved_categories__')

        if 'price' in data and data['price'] is not None:
            q = Decimal('0.01')
            data['price'] = (Decimal(data['price']).quantize(q, rounding=ROUND_HALF_UP))

        return data


class ProductResponseSchema(ma.Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    category = fields.Method('get_categories')
    price = fields.Decimal(places=2)
    owner_id = fields.Int()
    publish_date = fields.Date()
    fab_date = fields.Date(allow_none=True)
    exp_date = fields.Date(allow_none=True)
    
    
    def get_categories(self, schema):
        return [cat.name for cat in getattr(schema, 'categories', [])]
    
    @post_dump
    def drop_nulls(self, data, **kwargs):
        return {key: value for key, value in data.items() if value is not None}