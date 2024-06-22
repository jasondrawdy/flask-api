"""
Import all created endpoint objects in order to access them in a
clean and more user-friendly manner throughout the entire codebase.
"""
#! These are necessary in order to allow endpoints to properly load and work.
from .users.user import User
from .users.userlist import UserList
from .sessions.session import Session
from .sessions.sessionlist import SessionList
from .sessions.sessioncreate import SessionCreate
from .auth.authlogin import AuthLogin
from .auth.authlogout import AuthLogout
from .auth.authregister import AuthRegister
from .auth.authreset import AuthReset

#? Only for developers and should be removed before going into production.
#? NOTE: The endpoint/model can still exist, but to allow/disallow access just remove or comment the import line.
from .testing.test import Testing