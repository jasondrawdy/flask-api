from flask import session
from requests import request
from flask_restful import Resource, Api, abort
from database import db, query
from settings import Settings
from models import *
from utils.decorators import login_required

ARGS = ['user_id']

class AuthLogout(Resource):
    @login_required
    def post(self: "AuthLogout"): #* CREATE operation.
        try: args = args_parser.parse_args()
        except: abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid or null parameters provided.')
        if check_args_for_sameness(args, ARGS):
            user_id = args['user_id']
            session_user_id = session.get('_user_id', None)
            user = query(Users).get(user_id)
            if not user: 
                #? Just say they aren't logged in so they go away since we 
                #? don't want to expose what users are actually in the DB.
                abort(Settings.RESPONSE_CODES.BAD_REQUEST, message="You are not logged in!")
            if not session_user_id:
                abort(Settings.RESPONSE_CODES.BAD_REQUEST, message="You are not logged in!")
            if int(session_user_id) == int(user_id):
                session.pop('_user_id')
                session.pop('_id')
                url = f"{Settings.BASE_URL}/sessions/{user_id}"
                headers = {'internal-api-token': Settings.CONFIG['tokens']['internal-api-token']}
                response = request(method="DELETE", url=url, headers=headers)
                if response.status_code == Settings.RESPONSE_CODES.OK:
                    user.authenticated = False
                    db.session.commit()
                    return "You are now logged out.", Settings.RESPONSE_CODES.OK
                else:
                    message = response.content.decode('utf-8').strip().strip("\"")
                    abort(Settings.RESPONSE_CODES.BAD_REQUEST, message=message)
            else:
                abort(Settings.RESPONSE_CODES.UNAUTHORIZED, message="The provided user id is invalid.")
        else:
            abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid or null parameters provided.')
            
    @staticmethod
    def register_args():
        for arg in ARGS:
            args_parser.add_argument(arg)
            
    @staticmethod
    def register_routes(api: Api):
        api.app.logger.info(f"Registering '{__name__}' routes..")
        api.add_resource(AuthLogout, f'{Settings.BASE_ROUTE}/auth/logout')