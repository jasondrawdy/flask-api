from datetime import datetime
from flask_restful import Resource, Api, abort
from utils.decorators import internal_only, login_required
from utils.security import Hashing, Passwords
from database import db, query
from settings import Settings
from models import *

ARGS = ['username', 'password', 'first_name', 'last_name', 'email']

class UserList(Resource):
    @internal_only
    def get(self: "UserList"): #* READ operation.
        result = [user.as_dict() for user in query(Users).all()]
        users = {result.index(entry)+1: entry for entry in result}
        return users, Settings.RESPONSE_CODES.OK
    
    @internal_only
    def post(self: "UserList"): #* CREATE operation.
        args = args_parser.parse_args()
        if check_args_for_sameness(args, ARGS):
            provided_username = args['username']
            provided_password = args['password']
            provided_email = args['email']
            username_exists = query(Users).filter(Users.username == provided_username).first()
            email_exists = query(Users).filter(Users.email == provided_email).first()
            if username_exists:
                abort(Settings.RESPONSE_CODES.CONFLICT, message="That username already exists!")
            if email_exists:
                abort(Settings.RESPONSE_CODES.CONFLICT, message="That email already exists!")
            salt = Passwords.generate_salt()
            pepper = Passwords.generate_pepper(salt, provided_password)
            password = Hashing.calculate_message_hash(f'{salt}{provided_password}{pepper}')
            user = Users(
                username=provided_username,
                password=password,
                salt=salt,
                email=provided_email,
                first_name=args['first_name'],
                last_name=args['last_name'],
                created_on=datetime.now(),
                admin=False,
                authenticated=False
            )
            db.session.add(user)
            db.session.commit()
            return user.as_dict(), Settings.RESPONSE_CODES.CREATED
        else:
            abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid or null parameters provided.')
            
    @staticmethod
    def register_args():
        for arg in ARGS:
            args_parser.add_argument(arg)
            
    @staticmethod
    def register_routes(api: Api):
        api.app.logger.info(f"Registering '{__name__}' routes..")
        api.add_resource(UserList, f'{Settings.BASE_ROUTE}/users')