from marshmallow import fields, validate, ValidationError
from app import marshmallow
from app.models import User

def ensure_unique_user(data):
    user = User.query.filter(User.email == data).first()
    if user:
        raise ValidationError('Email already exists')


class UserSchema(marshmallow.Schema):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password_hash')


class RegistrationSchema(marshmallow.Schema):
    first_name = fields.Str(required=True, validate=[validate.Length(min=1, max=100)])
    last_name = fields.Str(required=True, validate=[validate.Length(min=1, max=100)])
    email = fields.Email(required=True, validate = ensure_unique_user)
    password = fields.Str(required=True, validate=[validate.Length(min=8, max=200)] )


class AuthSchema(marshmallow.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=[validate.Length(min=8, max=200)])


class RequestResetPasswordSchema(marshmallow.Schema):
    email = fields.Email(required=True, validate=ensure_unique_user)


class ResetPasswordSchema(marshmallow.Schema):
    email = fields.Email(required=True, validate=ensure_unique_user)
    password = fields.Str(required=True, validate=[validate.Length(min=8, max=200)])

class CreatePasswordSchema(marshmallow.Schema):
    password = fields.Str(required=True, validate=[validate.Length(min=8, max=200)])

class ChangePasswordSchema(marshmallow.Schema):
    old_password = fields.Str(required=True, validate=[validate.Length(min=8, max=200)])
    new_password = fields.Str(required=True, validate=[validate.Length(min=8, max=200)])


users_schema = UserSchema(many=True)
auth_schema = AuthSchema()
registration_schema = RegistrationSchema()
request_reset_password_schema = RequestResetPasswordSchema()
reset_password_schema = ResetPasswordSchema()
create_password_schema = CreatePasswordSchema()
change_password_schema = ChangePasswordSchema()


