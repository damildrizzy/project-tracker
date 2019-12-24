from flask import request, jsonify
from app.account.schema import users_schema, registration_schema
from app.models import User
from app import db
from flask_restful import Resource
from app.decorators import admin_required
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies
)


class UserView(Resource):
    @admin_required
    @jwt_required
    def get(self):
        users = User.query.all()
        response = {
            'data': users_schema.dump(users)
        }
        return response, 200

    
    def post(self):
        json_data = request.get_json()

        if not json_data:
            response = {
                'error': 'Invalid Input'
            }
            return response, 400
        
        data = registration_schema.load(json_data)

        # if errors:
        #     response = {
        #         'error': errors
        #     }
        #     return jsonify(response), 422
        
        user = User()
        user.email = data.get('email')
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.password = data.get('password')
        db.session.add(user)
        db.session.commit()

        return data, 200





