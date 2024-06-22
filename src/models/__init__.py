"""
Import all data models here for easier, and cleaner, access across the codebase.
"""
from flask_restful import reqparse, abort
from database import query
from settings import Settings
from .auth.db_resetrequests import ResetRequests
from .users.db_users import Users
from .roles.db_roles import Roles
from .roles.db_roletypes import RoleTypes
from .roles.db_rolepermissions import RolePermissions
from .roles.db_rolepermissiontypes import RolePermissionTypes
from .carriers.db_carriers import Carriers
from .sessions.db_sessions import Sessions
from .config.db_tokens import Tokens
from .network.db_servicerequests import ServiceRequests
args_parser = reqparse.RequestParser()
        
def abort_if_user_doesnt_exist(user_id):
    user = query(Users).get(user_id)
    if not user:
        abort(Settings.RESPONSE_CODES.NOT_FOUND, message=f"A user with id of '{user_id}' does not exist.")
    return user

def try_casting_endpoint_parameter(endpoint, data):
    data_types = {
        "UserList": int,
        "User": int,
        "UserRoles": int,
        "UserSessions": int,
    }
    try:
        data_type = data_types.get(endpoint)
        return data_type(data)
    except:
        return None
    
def check_args_for_sameness(args: dict, endpoint_args: dict):
    for arg in endpoint_args:
        data = args[arg]
        if not arg in list(args.keys()):
            return False
        if data is None or data.strip() == "":
            return False
    return True