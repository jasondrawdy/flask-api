from flask_restful import Resource, Api
from utils.decorators import rate_limit
from utils.security import Passwords
from settings import Settings
from models import *

class Testing(Resource):
    @rate_limit
    def get(self: "Testing"): #* READ operation.
        return Passwords.generate_cid(), Settings.RESPONSE_CODES.OK
    
    @staticmethod
    def register_routes(api: Api):
        api.app.logger.info(f"Registering '{__name__}' routes..")
        api.add_resource(Testing, f'{Settings.BASE_ROUTE}/testing')