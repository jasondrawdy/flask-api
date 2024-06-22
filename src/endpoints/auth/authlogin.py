import json
from datetime import datetime
from flask import session
from requests import request
from utils.security import Hashing, Passwords
from flask_restful import Resource, Api, abort
from database import db, query
from settings import Settings
from models import *

ARGS = ['username', 'password']

class AuthLogin(Resource):
    def post(self: "AuthLogin"): #* CREATE operation.
        if '_user_id' in session:
            abort(Settings.RESPONSE_CODES.NOT_ACCEPTABLE, message="You're already logged in!")
        args = args_parser.parse_args()
        if check_args_for_sameness(args, ARGS):
            username = args['username']
            password = args['password']
            user = query(Users).filter(Users.username == username).first()
            if not user:
                abort(Settings.RESPONSE_CODES.UNAUTHORIZED, message="Invalid credentials provided.")
            salt = user.salt
            pepper = Passwords.generate_pepper(salt, password)
            hashed_password = Hashing.calculate_message_hash(f"{salt}{password}{pepper}")
            if hashed_password == user.password:
                user.last_login = datetime.now()
                url = f"{Settings.BASE_URL}/sessions/create"
                body = {'user_id': user.id}
                headers = {'internal-api-token': Settings.CONFIG['tokens']['internal-api-token']}
                response = request(method="POST", url=url, json=body, headers=headers)
                if response.status_code == Settings.RESPONSE_CODES.CREATED:
                    token = json.loads(response.content.decode())['token']
                    session['_user_id'] = user.id
                    session['_id'] = token
                    user.authenticated = True
                    db.session.commit()
                    data = user.for_web()
                    data['token'] = token
                    return data, Settings.RESPONSE_CODES.OK
                else:
                    result = query(Sessions).filter(Sessions.expires_on > datetime.now(), Sessions.id == user.id).first()
                    if result:
                        session['_user_id'] = user.id
                        session['_id'] = result.token
                        user.authenticated = True
                        db.session.commit()
                        data = user.for_web()
                        data['token'] = result.token
                        return data, Settings.RESPONSE_CODES.OK
                    else:
                        abort(Settings.RESPONSE_CODES.GONE, message="No session could be found or created.")
            else:
                abort(Settings.RESPONSE_CODES.UNAUTHORIZED, message="Invalid credentials provided.")
        else:
            abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid or null parameters provided.')

    @staticmethod
    def register_args():
        for arg in ARGS:
            args_parser.add_argument(arg)
            
    @staticmethod
    def register_routes(api: Api):
        api.app.logger.info(f"Registering '{__name__}' routes..")
        api.add_resource(AuthLogin, f'{Settings.BASE_ROUTE}/auth/login')