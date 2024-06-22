from datetime import datetime, timedelta
from flask import request, session, abort
from functools import wraps
from settings import Settings
from database import db
from models import *

def internal_only(original_function):
    @wraps(original_function)
    def function_wrapper(*args, **kwargs):
        localhost = ["0.0.0.0", "127.0.0.1"]
        try:
            if request.remote_addr not in localhost:
                return None, Settings.RESPONSE_CODES.NOT_FOUND
            nullset = ['', " ", None]
            headers = request.headers
            if 'internal-api-token' not in headers: #? Used for internal API communication.
                return "Credentials not present in request!", Settings.RESPONSE_CODES.UNAUTHORIZED
            elif 'internal-api-token' in headers and headers['internal-api-token'] in nullset:
                return "No value set for internal-api-token!", Settings.RESPONSE_CODES.UNAUTHORIZED
            elif headers['internal-api-token'] != Settings.CONFIG['tokens']['internal-api-token']: # Loaded from DB.
                return "The provided credentials are NOT valid.", Settings.RESPONSE_CODES.UNAUTHORIZED
        except:
            return (
                'Invalid headers or request payload. Please refer to the API documentation for help.', 
                Settings.RESPONSE_CODES.BAD_REQUEST
            )
        return original_function(*args, **kwargs)
    return function_wrapper

def login_required(original_function):
    @wraps(original_function)
    def function_wrapper(*args, **kwargs):
        if not "_user_id" in session:
            abort(Settings.RESPONSE_CODES.UNAUTHORIZED, message="Please login!")
        return original_function(*args, **kwargs)
    return function_wrapper

def admin_required(original_function): # Pair this with login_required first for maximum effect and no errors.
    @wraps(original_function)
    def function_wrapper(*args, **kwargs):
        user_id = session['_user_id']
        user: Users = query(Users).get(int(user_id))
        if not user:
            abort(Settings.RESPONSE_CODES.UNAUTHORIZED, message="Invalid user id!")
        if not user.is_admin():
            abort(Settings.RESPONSE_CODES.UNAUTHORIZED, message="Administrators only!")
        return original_function(*args, **kwargs)
    return function_wrapper

def rate_limit(original_function):
    @wraps(original_function)
    def function_wrapper(*args, **kwargs):
        user_id = session['_user_id'] if "_user_id" in session else "N/A"
        now = datetime.now()
        n_hours_ago = now - timedelta(hours=1)
        request_limit = 10 # Normally 1000 per hour; And this is just a static variable to extend upon in the future instead of making it highly embedded.
        requests = query(ServiceRequests).filter(ServiceRequests.created_on > n_hours_ago).filter(ServiceRequests.created_on < now).all()
        if len(requests) >= request_limit:
            abort(Settings.RESPONSE_CODES.FORBIDDEN, message="Rate limit has been reached! Please try again in an hour.")
        # Add an entry to the db and keep going.
        service_request = ServiceRequests(
            user_id=str(user_id),
            request_ip=str(request.remote_addr),
            request_origin=str(request.referrer),
            request_destination=str(request.url),
            created_on=now
        )
        db.session.add(service_request)
        db.session.commit()
        return original_function(*args, **kwargs)
    return function_wrapper

# TODO: MAKE A RATE LIMIT FUNCTION!