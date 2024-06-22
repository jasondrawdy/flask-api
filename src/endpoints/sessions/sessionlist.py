from flask_restful import Resource, Api
from utils.decorators import internal_only
from database import db, query
from settings import Settings
from models import *

class SessionList(Resource):
    @internal_only
    def get(self: "SessionList"): #* READ operation.
        result = [session.as_dict() for session in query(Sessions).all()]
        sessions = {result.index(entry)+1: entry for entry in result}
        return sessions
            
    @staticmethod
    def register_routes(api: Api):
        api.app.logger.info(f"Registering '{__name__}' routes..")
        api.add_resource(SessionList, f'{Settings.BASE_ROUTE}/sessions')