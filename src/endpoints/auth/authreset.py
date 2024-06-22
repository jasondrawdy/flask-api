from datetime import datetime
from flask_restful import Resource, Api, abort
from database import db, query
from settings import Settings
from models import *

ARGS = ['email']

class AuthReset(Resource):
    def post(self: "AuthReset"): #* CREATE operation.
        args = args_parser.parse_args()
        if check_args_for_sameness(args, ARGS):
            email = args['email']
            total_reset_requests = query(ResetRequests).filter(ResetRequests.email == email).count()
            user_exists = query(Users.id).filter_by(email=email).first() is not None
            if not user_exists:
                abort(Settings.RESPONSE_CODES.BAD_REQUEST, message="A user with that email does not exist.")
            if total_reset_requests > 0:
                abort(Settings.RESPONSE_CODES.BAD_REQUEST, message="You have already requested a password reset.")
            request = ResetRequests(
                email=email,
                time_requested=datetime.now(),
                time_resolved=None
            )
            db.session.add(request)
            db.session.commit()
            return "A password reset has been requested!", Settings.RESPONSE_CODES.OK
        else:
            abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid or null parameters provided.')

    @staticmethod
    def register_args():
        for arg in ARGS:
            args_parser.add_argument(arg)
            
    @staticmethod
    def register_routes(api: Api):
        api.app.logger.info(f"Registering '{__name__}' routes..")
        api.add_resource(AuthReset, f'{Settings.BASE_ROUTE}/auth/reset')