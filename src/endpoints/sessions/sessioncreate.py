from hashlib import sha512
from flask import request, session
from flask_restful import Resource, Api, abort
from datetime import datetime, timedelta
from utils.decorators import internal_only, login_required
from database import db, query
from settings import Settings
from models import *

from utils.generators import TextUtils

ARGS = ['user_id']

class SessionCreate(Resource):
    def _hash_data(self: "SessionCreate", data: str):
        hasher = sha512(data.encode('utf-8'))
        return hasher.digest().hex()
    
    @internal_only
    def post(self: "SessionCreate"): #* CREATE operation.
        args = args_parser.parse_args()
        if check_args_for_sameness(args, ARGS):
            user: Users = query(Users).get(args['user_id'])
            if not user:
                abort(Settings.RESPONSE_CODES.BAD_REQUEST, message="No user with that ID exists.")
            current_sessions = query(Sessions).filter(Sessions.user_id == user.id).count()
            if current_sessions > 0:
                abort(Settings.RESPONSE_CODES.BAD_REQUEST, message="You have already created a session!")
            session_id = f"star-{self._hash_data(f'{user.email}{TextUtils.generate_cid()}')}"
            original_signature = self._hash_data(f"{user.id}{session_id}{Settings.APP.secret_key}")
            current_session = Sessions(
                user_id=user.id,
                started_on=datetime.now(),
                expires_on=datetime.now() + timedelta(hours=12),
                original_signature = original_signature,
                token=session_id,
                ip=request.remote_addr
            )
            db.session.add(current_session)
            db.session.commit()
            return {"token": session_id}, Settings.RESPONSE_CODES.CREATED
        else:
            abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid or null parameters provided.')

    @staticmethod
    def register_args():
        for arg in ARGS:
            args_parser.add_argument(arg)
            
    @staticmethod
    def register_routes(api: Api):
        api.app.logger.info(f"Registering '{__name__}' routes..")
        api.add_resource(SessionCreate, f'{Settings.BASE_ROUTE}/sessions/create')