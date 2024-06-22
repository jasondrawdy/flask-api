from datetime import datetime
from flask_restful import Resource, Api, abort
from utils.decorators import internal_only, login_required
from utils.security import Hashing, Passwords
from database import db, query
from settings import Settings
from models import *
from utils.logger import Logger
log = Logger(__name__)

ARGS = ['username', 'password', 'first_name', 'last_name', 'email']

class User(Resource):
    @internal_only
    def get(self, user_id): #* READ operation
        try:
            user_id = try_casting_endpoint_parameter('User', user_id)
            if user_id is None:
                abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid data format for user_id.')
            else:
                # The following abort function already gets the user, so just use
                # that instead of querying the db again for another instance.
                user: Users = abort_if_user_doesnt_exist(user_id)
                return user.as_dict(), Settings.RESPONSE_CODES.OK
        except Exception as error:
            log.error(f"ERROR: {error}")
    
    @internal_only
    def delete(self, user_id): #* DELETE operation
        try:
            user_id = try_casting_endpoint_parameter('User', user_id)
            if user_id is None:
                abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid data format for user_id.')
            else:
                user: Users = abort_if_user_doesnt_exist(user_id)
                db.session.delete(user)
                db.session.commit()
                return 'Successfully deleted user!', Settings.RESPONSE_CODES.OK
        except Exception as error:
            log.error(f"ERROR: {error}")
    
    @internal_only
    def put(self, user_id): #* UPDATE operation
        args = args_parser.parse_args()
        if check_args_for_sameness(args, ARGS):
            provided_username = args['username']
            provided_password = args['password']
            provided_email = args['email']
            original_user = query(Users).get(user_id)
            username_exists = query(Users).filter(Users.username == provided_username).first()
            email_exists = query(Users).filter(Users.email == provided_email).first()
            if username_exists and username_exists.username == provided_username:
                if provided_username != original_user.username:
                    abort(Settings.RESPONSE_CODES.CONFLICT, message="That username already exists!")
            if email_exists and email_exists.email == provided_email:
                if provided_email != original_user.email:
                    abort(Settings.RESPONSE_CODES.CONFLICT, message="That email already exists!")
            user_id = try_casting_endpoint_parameter('User', user_id)
            if user_id is None:
                abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid data format for user_id.')
            else:
                # TODO: Allow updating only parts of the user object.
                salt = Passwords.generate_salt()
                pepper = Passwords.generate_pepper(salt, provided_password)
                password = Hashing.calculate_message_hash(f"{salt}{provided_password}{pepper}")
                user: Users = abort_if_user_doesnt_exist(user_id)
                user.username = provided_username
                user.password = password
                user.salt = salt
                user.email = provided_email
                user.first_name = args['first_name']
                user.last_name = args['last_name']
                user.updated_on = datetime.now()
                try: db.session.commit()
                except:
                    abort(Settings.RESPONSE_CODES.INTERNAL_SERVER_ERROR)
                return 'Successfully updated user!', Settings.RESPONSE_CODES.OK
        else:
            abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid or null parameters provided.')
    
    @staticmethod
    def register_args():
        if ARGS:
            for arg in ARGS:
                args_parser.add_argument(arg)
            
    @staticmethod
    def register_routes(api: Api):
        api.app.logger.info(f"Registering '{__name__}' routes..")
        api.add_resource(User, f'{Settings.BASE_ROUTE}/users/<user_id>')