from marshmallow import fields, validate, validates, ValidationError, post_load
from app.libraries import ma
from models.enums import RolesEnum
from decimal import Decimal
import re
from datetime import date as dt_date


class UserCreateSchema(ma.Schema):
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=30), 
        error_messages={
            'required': 'Username é um campo obrigatório',
            'invalid': 'Username deve ser uma string válida'
        })
    
    email = fields.Email(
        required=True, 
        validate=validate.Length(max=130), 
        error_messages={
            'required': 'Email é um campo obrigatório',
            'invalid': 'Email deve ter formato válido'
        })
    
    password = fields.Str(
        required=True, 
        validate=validate.Length(min=8, max=128), 
        error_messages={
            'required': 'Senha é obrigatória',
            'invalid': 'Senha deve ser uma string válida'
            })
    
    first_name = fields.Str(
        required=True, 
        validate=validate.Length(min=2, max=30), 
        error_messages={
            'required': 'Nome é obrigatório',
            'invalid': 'Nome deve ser uma string válida'
        })
    
    last_name = fields.Str(
        required=True, 
        validate=validate.Length(min=2, max=50), 
        error_messages={
            'required': 'Nome é obrigatório',
            'invalid': 'Nome deve ser uma string válida'
        })
    
    birth_date = fields.Date(
        required=True, 
        error_messages={
            'invalid': 'Data de nascimento deve ter formato válido (YYYY-MM-DD)'
        })
    
    address = fields.Str(
        allow_none=True, 
        validate=validate.Length(max=200), 
        error_messages={
            'invalid': 'Endereço deve ser uma string válida'
        })
    
    phone = fields.Str(
        allow_none=True, 
        validate=validate.Length(max=24), 
        error_messages={
            'invalid': 'Telefone deve ser uma string válida'
        })
    
    role = fields.Enum(
        RolesEnum,
        by_value=True,
        allow_none=True,
        load_default=getattr(RolesEnum, 'USER', 'user'),
        error_messages={
            'invalid': 'Role deve ser "admin" ou "user"'
        })
    
    
    @validates('username')
    def validate_username(self, value, **kwargs):
        if not value or not value.strip():
            raise ValidationError('Username não pode estar vazio')

        regex_username = r'^[a-zA-Z0-9_\.]+$'
        if not re.match(regex_username, value):
            raise ValidationError('Username deve conter apenas letras, números e underscore e ponto')
    
    
    @validates('password')
    def validate_password(self, value, **kwargs):
        if not value:
            raise ValidationError('Senha não pode estar vazia')

        if not re.search(r'[a-zA-Z]', value):
            raise ValidationError('Senha deve conter pelo menos uma letra')

        # TODO: senha deve conter pelo menos uma letra maíscula

        if not re.search(r'[0-9]', value):
            raise ValidationError('Senha deve conter pelo menos um número')
    
    
    @validates('first_name')
    def validate_first_name(self, value, **kwargs):
        if not value or not value.strip():
            raise ValidationError('Nome não pode estar vazio')
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', value.strip()):
            raise ValidationError('Nome deve conter apenas letras')


    @validates('last_name')
    def validate_last_name(self, value, **kwargs):
        if not value or not value.strip():
            raise ValidationError('Sobrenome não pode estar vazio')
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', value.strip()):
            raise ValidationError('Sobrenome deve conter apenas letras')
    
    
    @validates('birth_date')
    def validate_birth_date(self, value, **kwargs):
        if not value:
            raise ValidationError('Data de nascimento não pode ser vazia')
        
        today = value.today()
        if value >= today:
            raise ValidationError('Data de nascimento deve ser anterior à data atual')

        age = today.year - value.year - \
            ((today.month, today.day) < (value.month, value.day))
        if age < 14:
            raise ValidationError('Usuário deve ter pelo menos 14 anos')
    
    
    # TODO: validate address
    
    
    @validates('phone')
    def validate_phone(self, value, **kwargs):
        if not value:
            raise ValidationError('Telefone não pode ser vazio')
        
        clean_phone = re.sub(r'[^\d]', '', value)
        if len(clean_phone) < 10 or len(clean_phone) > 15:
            raise ValidationError('Telefone deve ter entre 10 e 15 dígitos')
    
    
    @post_load
    def normalize_data(self, data, **kwargs):
        data['username'] = data['username'].strip().lower()
        data['email'] = data['email'].strip().lower()
        data['first_name'] = data['first_name'].strip().title()
        data['last_name'] = data['last_name'].strip().title()

        if data.get('address'):
            data['address'] = data['address'].strip()

        if data.get('phone'):
            data['phone'] = data['phone'].strip()

        if not data.get('role'):
            data['role'] = 'user'

        return data
    
    
class UserUpdateSchema(ma.Schema):
    first_name = fields.Str(
        allow_none=True, 
        validate=validate.Length(min=2, max=30), 
        error_messages={
            'invalid': 'Nome deve ser uma string válida'
        })
    
    last_name = fields.Str(required=True, 
        allow_none=True,
        validate=validate.Length(min=2, max=50), 
        error_messages={
            'invalid': 'Sobrenome deve ser uma string válida'
        })
    
    address = fields.Str(
        allow_none=True, 
        validate=validate.Length(max=200), 
        error_messages={
            'invalid': 'Endereço deve ser uma string válida'
        })
    
    phone = fields.Str(
        allow_none=True, 
        validate=validate.Length(max=24), 
        error_messages={
            'invalid': 'Telefone deve ser uma string válida'
        })
    
    balance = fields.Decimal(
        allow_none=True,
        places=2,
        as_string=True,
        validate=validate.Range(min=0, error='Saldo deve ser maior ou igual a 0'),
        error_messages={
            'invalid': 'Saldo deve ser um número válido'
        })
    
    
    @validates('first_name')
    def validate_first_name(self, value, **kwargs):
        if value is None:
            return
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', value.strip()):
            raise ValidationError('Nome deve conter apenas letras')


    @validates('last_name')
    def validate_last_name(self, value, **kwargs):
        if value is None:
            return
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', value.strip()):
            raise ValidationError('Sobrenome deve conter apenas letras')
 
    
    # TODO: validate address
    
    
    @validates('phone')
    def validate_phone(self, value, **kwargs):
        if value is None:
            return
        clean_phone = re.sub(r'[^\d]', '', value)
        if len(clean_phone) < 10 or len(clean_phone) > 15:
            raise ValidationError('Telefone deve ter entre 10 e 15 dígitos')


    @validates('balance')
    def validate_balance(self, value, **kwargs):
        if value is None:
            return
        if isinstance(value, str):
            try:
                Decimal(value)
            except Exception:
                raise ValidationError('Saldo deve ser numérico.')

    
    @post_load
    def normalize_data(self, data, **kwargs):
        if data.get('first_name'):
            data['first_name'] = data['first_name'].strip().title()

        if data.get('last_name'):
            data['last_name'] = data['last_name'].strip().title()

        if data.get('address'):
            data['address'] = data['address'].strip()

        if data.get('phone'):
            data['phone'] = data['phone'].strip()
            
        if data.get('balance'):
            data['balance'] = data['balance'].strip()

        return data


class ChangePasswordSchema(ma.Schema):
    current_password = fields.Str(
        required=True,
        error_messages={
            'required': 'Senha atual é obrigatória',
            'invalid': 'Senha atual deve ser uma string válida'
        })

    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128),
        error_messages={
            'required': 'Nova senha é obrigatória',
            'invalid': 'Nova senha deve ser uma string válida'
        })

    confirm_password = fields.Str(
        required=True,
        error_messages={
            'required': 'Confirmação de senha é obrigatória',
            'invalid': 'Confirmação de senha deve ser uma string válida'
        })


    @validates('new_password')
    def validate_new_password(self, value, **kwargs):
        if not value:
            raise ValidationError('Nova senha não pode estar vazia')

        if not re.search(r'[a-zA-Z]', value):
            raise ValidationError('Nova senha deve conter pelo menos uma letra')

        # TODO: senha deve conter pelo menos uma letra maíscula

        if not re.search(r'[0-9]', value):
            raise ValidationError('Nova senha deve conter pelo menos um número')


    @validates('confirm_password')
    def validate_confirm_password(self, value, **kwargs):
        if not value:
            raise ValidationError('Confirmação de senha não pode estar vazia')


    @post_load
    def validate_passwords_match(self, data, **kwargs):
        if data.get('new_password') != data.get('confirm_password'):
            raise ValidationError({'confirm_password': 'Confirmação de senha não coincide com nova senha'})
        return data


class UserResponseSchema(ma.Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    full_name = fields.Method('get_full_name')
    first_name = fields.Str()
    last_name = fields.Str()
    balance = fields.Decimal(places=2)
    birth_date = fields.Date()
    phone = fields.Str()
    role = fields.Str()
    is_active = fields.Bool()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'