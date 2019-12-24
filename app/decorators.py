from functools import wraps

from app.models import User

from flask import abort, jsonify, make_response

from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request, create_access_token,
    get_jwt_claims, get_jwt_identity, current_user
)
#from flask_login import current_user


#from app.models import Permission


# def permission_required(permission):
#     """Restrict a view to users with the given permission."""

#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if not current_user.can(permission):
#                 abort(403)
#             return f(*args, **kwargs)

#         return decorated_function

#     return decorator


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        user = User.query.filter_by(email = current_user).first()
        if not user.is_admin():
            return make_response(jsonify(msg='Admins only!'), 403)
        else:
            return fn(*args, **kwargs)
    return wrapper


