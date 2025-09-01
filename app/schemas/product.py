from marshmallow import fields, validate, validates, ValidationError, post_load, validates_schema, post_dump
from app.libraries import ma, db
from decimal import Decimal, ROUND_HALF_UP
from app.libraries import norm
from models.user import User
from models.category import Category
from models.enums import Perishables
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
        normalized = {norm(x) for x in cat_names if isinstance(x, str)}
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


class ProductUpdateSchema(ma.Schema):
    name        = fields.Str(allow_none=True, validate=validate.Length(min=3, max=30))
    description = fields.Str(allow_none=True, validate=validate.Length(min=3, max=180))
    categories  = fields.List(fields.Raw(), allow_none=True)
    price       = fields.Decimal(allow_none=True, as_string=True, places=2, validate=validate.Range(min=0))
    fab_date    = fields.Date(allow_none=True)
    exp_date    = fields.Date(allow_none=True)

    
    @validates('categories')
    def validate_categories(self, value, **kwargs):
        if value is None:
            return
        names, ids = [], []
        for v in value:
            if isinstance(v, int):
                ids.append(v)
            elif isinstance(v, str) and v.strip():
                names.append(v.strip())
            else:
                raise ValidationError('Categorias devem ser nomes (str) ou ids (int).')

        rows = []
        if ids:
            rows += Category.query.filter(Category.id.in_(ids)).all()
        if names:
            rows += Category.query.filter(Category.name.in_(names)).all()

        seen, resolved = set(), []
        for c in rows:
            if c.id not in seen:
                seen.add(c.id)
                resolved.append(c)

        found_ids = {c.id for c in resolved}
        found_names = {c.name for c in resolved}
        missing_ids = [i for i in ids if i not in found_ids]
        missing_names = [n for n in names if n not in found_names]
        if missing_ids or missing_names:
            parts = []
            if missing_ids:
                parts.append(f"IDs inexistentes: {', '.join(map(str, missing_ids))}")
            if missing_names:
                parts.append(f"Nomes inexistentes: {', '.join(missing_names)}")
            raise ValidationError('; '.join(parts))

        self.context['__resolved_categories__'] = resolved

    
    @validates_schema
    def validate_dates(self, data, **kwargs):
        prod = self.context.get('product')

        # categorias finais: novas (se vieram) senão as atuais do produto
        if data.get('categories') is not None:
            cats = self.context.get('__resolved_categories__', [])
            final_names = [c.name for c in cats]
        else:
            final_names = [c.name for c in getattr(prod, 'categories', [])] if prod else []

        perishable = any(norm(n) in Perishables for n in final_names)

        fab = data.get('fab_date') or (getattr(prod, 'fab_date', None) if prod else None)
        exp = data.get('exp_date') or (getattr(prod, 'exp_date', None) if prod else None)
        pub = getattr(prod, 'publish_date', None)

        if perishable:
            missing = {}
            if fab is None: missing['fab_date'] = ['fab_date é obrigatório para produtos perecíveis.']
            if exp is None: missing['exp_date'] = ['exp_date é obrigatório para produtos perecíveis.']
            if missing:
                raise ValidationError(missing)

        if fab and exp and fab >= exp:
            raise ValidationError({'exp_date': 'exp_date deve ser maior que fab_date.'})
        if exp and pub and exp <= pub:
            raise ValidationError({'exp_date': 'exp_date deve ser maior que publish_date.'})
    
    
    @post_load
    def normalize(self, data, **kwargs):
        if data.get('name') is not None:
            data['name'] = data['name'].strip().title()
        if data.get('description') is not None:
            data['description'] = data['description'].strip()
        if data.get('price') is not None:
            data['price'] = Decimal(str(data['price'])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if 'categories' in data:
            data['categories'] = self.context.pop('__resolved_categories__', [])
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