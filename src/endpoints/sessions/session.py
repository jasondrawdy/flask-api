from flask_restful import Resource, Api, abort
from utils.decorators import internal_only, login_required
from database import db, query
from settings import Settings
from models import *

class Session(Resource):
    @internal_only
    def get(self, user_id): #* READ operation
        if not user_id:
            abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid data format.')
        else:
            session = query(Sessions).filter(Sessions.user_id == user_id).order_by(Sessions.id.desc()).first()
            if session:
                return session.as_dict(), Settings.RESPONSE_CODES.OK
            else:
                abort(Settings.RESPONSE_CODES.NOT_FOUND, message="No session was found.")
    
    @internal_only
    def delete(self, user_id): #* DELETE operation
        if not user_id:
            abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='Invalid data format.')
        else:
            sessions = db.session.query(Sessions).filter(Sessions.user_id == user_id).all()
            if len(sessions) > 0:
                for session in sessions:
                    db.session.delete(session)
                    db.session.commit()
                return 'Successfully deleted all user sessions!', Settings.RESPONSE_CODES.OK
            else:
                abort(Settings.RESPONSE_CODES.BAD_REQUEST, message='No sessions were found.')
    
    @staticmethod
    def register_routes(api: Api):
        api.app.logger.info(f"Registering '{__name__}' routes..")
        api.add_resource(Session, f'{Settings.BASE_ROUTE}/sessions/<int:user_id>')