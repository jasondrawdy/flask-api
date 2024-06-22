from requests import request
from flask_restful import Resource, Api, abort
from database import db, query
from settings import Settings
from models import *

ARGS = ['username', 'password', 'first_name', 'last_name', 'email']

class AuthRegister(Resource):
    def post(self: "AuthRegister"): #* CREATE operation.
        args = args_parser.parse_args()
        if check_args_for_sameness(args, ARGS):
            username = args['username']
            email = args['email']
            username_exists = query(Users).filter(Users.username == username).first()
            email_exists = query(Users).filter(Users.email == email).first()
            if username_exists and username_exists.username == username:
                abort(Settings.RESPONSE_CODES.UNAUTHORIZED, message="That username already exists!")
            if email_exists and email_exists.email == email:
                abort(Settings.RESPONSE_CODES.UNAUTHORIZED, message="That email already exists!")
            url = f"{Settings.BASE_URL}/users"
            body = args
            headers = {'internal-api-token': query(Tokens).filter(Tokens.name == "internal-api-token").first().value}
            response = request(method="POST", url=url, json=body, headers=headers)
            if response.status_code == Settings.RESPONSE_CODES.CREATED:
                return "Account successfully created!", Settings.RESPONSE_CODES.CREATED
            else:
                message = response.content.decode('utf-8').strip().strip("\"")
                abort(Settings.RESPONSE_CODES.NOT_ACCEPTABLE, message=message)
        else:
            abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid or null parameters provided.')

    @staticmethod
    def register_args():
        for arg in ARGS:
            args_parser.add_argument(arg)
            
    @staticmethod
    def register_routes(api: Api):
        api.app.logger.info(f"Registering '{__name__}' routes..")
        api.add_resource(AuthRegister, f'{Settings.BASE_ROUTE}/auth/register')
        
        
"""
curl -H 'Content-Type: application/json' \
      -d '{ "username":"jason","password":"testing", "first_name":"Jason", "last_name":"ADMIN", "email":"testing@email.com"}' \
      -X POST \
      http://0.0.0.0:8000/api/v1/auth/register
"""