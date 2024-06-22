import sys
import inspect
import endpoints
import asyncio
from flask import Flask
from flask_restful import Api
from database import db, init_db
from settings import Settings
from utils.security import Passwords, Hashing
from loaders.plugins import Plugins
from models import *

# Cleans __pycache__ files and is an optional import.
from utils.sentinel import Sentinel
sentinel = Sentinel()
sentinel.authorized = True #? False if you want __pycache__ files.
sentinel.start()
    
from utils.logger import Logger
from utils.colors import Colors
log = Logger(__name__)

class Service:
    def __init__(self: "Service") -> None:
        """Create a new instance of the service framework with any required dependencies."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.plugins = Plugins()
        self._init_security()
        self._init_database()
        self._init_endpoints()
        self._init_config() # EOL because we need to init the db first before syncing.
        
    def _init_config(self: "Service"):
        with self.app.app_context(): # Populate the config with tokens and other objects.
            token_list = query(Tokens).all() #? Used for internal API communication (verification & etc).
            if len(token_list) > 0:
                Settings.CONFIG['tokens'].update({token.name: token.value for token in token_list})
            else:
                log.warning("No \"internal-api-token\" found in the database!")
                api_token = Passwords.generate_cid() # These should be as random as possible and not user generated.
                token = Tokens(
                    name="internal-api-token",
                    value=api_token
                )
                db.session.add(token)
                db.session.commit()
                log.note("Generated a new \"internal-api-token\"!")
        Settings.APP = self.app
        if Settings.DEBUG:
            log.warning(f"{Colors.Foreground.yellow}====* THE CURRENT API IS BEING RUN IN DEBUG MODE! *===={Colors.reset}")
        asyncio.run(self.plugins.watch())

    def _init_security(self: "Service"):
        key = Passwords.generate_cid(64)
        salt = Passwords.generate_cid(128)
        pepper = Passwords.generate_pepper(salt, key)
        secret_key = Hashing.calculate_message_hash(f"{salt}{key}{pepper}")
        self.app.secret_key = secret_key.encode()
        
    def _init_database(self: "Service"):
        self.app.config["SESSION_COOKIE_SECURE"] = True
        self.app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
        self.app.config["SQLALCHEMY_DATABASE_URI"] = Settings.DATABASE_URI
        init_db(self.app, db)
        
    def _init_endpoints(self: "Service"):
        self.call_module_function(endpoints, "register_args")
        self.call_module_function(endpoints, "register_routes", self.api)
    
    def call_module_function(self: "Service", module_name, function_name, arg=None):
        """Iterates through all classes in a module and calls a specified function while also passing any provided args."""
        for name, obj in inspect.getmembers(module_name):
            if inspect.isclass(obj):
                if hasattr(obj, function_name) and callable(getattr(obj, function_name)):
                    registration_function = getattr(obj, function_name)
                    try: registration_function(arg)
                    except: registration_function()
    
    def add_token_to_database(self: "Service", token_name, token_value):
        token = Tokens(
            name=token_name,
            value=token_value
        )
        db.session.add(token)
        db.session.commit()
    
    def start(self: "Service"): #! DO NOT USE IN PRODUCTION!
        self.app.run(host=Settings.API_HOST, port=Settings.API_PORT, debug=True)
    
def create_service(): #! USE THIS WITH GUNICORN (or another WSGI server) INSTEAD OF THE ABOVE START FUNCTION.
    microservice = Service()
    return microservice.app

if __name__ == "__main__":
    # Start the service manually since we ran 'python main.py'.
    microservice = Service()
    microservice.start()