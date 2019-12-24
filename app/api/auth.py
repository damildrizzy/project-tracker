from flask import jsonify, request, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies, get_jwt_identity
)

from app.models import User
from app.account.schema import auth_schema


class AuthView(Resource):

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {
                'error': 'Invalid Input'
            }
        
        data = auth_schema.load(json_data)

        user = User.query.filter_by(email = data['email']).first()

        if not user:
            response = {
                'error': 'User does not exist'
            }
        
        if user.verify_password(data['password']):
            access_token = create_access_token(identity = data['email'])
            

            response = {
                'data': {
                    'message': f'Logged in as {user}',
                    'access_token': access_token,
                   
                }
            }
            return response

        else:
            response = {
                'error': 'Wrong password'
            }

    

    @jwt_required
    #see also: :func:~flask_jwt_extended.fresh_jwt_required
    def delete(self):
        response = jsonify({
            'data': {
                'logout': True
            }
        })
        response.status_code = 200
        # Because the JWTs are stored in an httponly cookie now, we cannot
        # log the user out by simply deleting the cookie in the frontend.
        # We need the backend to send us a response to delete the cookies
        # in order to logout. unset_jwt_cookies is a helper function to
        # do just that.
        unset_jwt_cookies(response)

        return response

    
    
    








