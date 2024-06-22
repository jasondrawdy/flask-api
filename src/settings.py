from dataclasses import dataclass
from sshtunnel import SSHTunnelForwarder

class WebRequests:
    @dataclass
    class HttpResponseCodes:
        #? This class of status codes indicates the action requested by the client was received, understood, and accepted.
        OK = 200
        CREATED = 201
        ACCEPTED = 202
        MODIFIED_INFORMATION = 203
        NO_CONTENT = 204
        RESET_CONTENT = 205
        PARTIAL_CONTENT = 206
        #? This class of status code indicates the client must take additional action to complete the request. 
        #? Many of these status codes are used in URL redirection.
        MULTIPLE_CHOICES = 300
        MOVED_PERMANENTLY = 301
        #? This class of status code is intended for situations in which the error seems to have been caused by the client.
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        PAYMENT_REQUIRED = 402
        FORBIDDEN = 403
        NOT_FOUND = 404
        METHOD_NOT_ALLOW = 405
        NOT_ACCEPTABLE = 406
        PROXY_AUTHENTICATION_REQUIRED = 407
        REQUEST_TIMEOUT = 408
        CONFLICT = 409
        GONE = 410
        LENGTH_REQUIRED = 411
        PRECONDITION_FAILED = 412
        PAYLOAD_TOO_LARGE = 413
        URI_TOO_LONG = 414
        UNSUPPORTED_MEDIA_TYPE = 415
        RANGE_NOT_SATISFIABLE = 416
        EXPECTATION_FAILED = 417
        IM_A_TEAPOT = 418
        TOO_MANY_REQUESTS = 429
        #? Response status codes beginning with the digit "5" indicate cases in which the server is aware that it 
        #? has encountered an error or is otherwise incapable of performing the request.
        INTERNAL_SERVER_ERROR = 500
        NOT_IMPLEMENTED = 501
        BAD_GATEWAY = 502
        SERVICE_UNAVAILABLE = 503
        GATEWAY_TIMEOUT = 504
        HTTP_VERSION_NOT_SUPPORTED = 505

class Settings:
    #!====================================================
    DEBUG = True #! CHANGE TO FALSE IN PRODUCTION.
    #!====================================================
    API_GENERATION = 'v1'  #? Can be anything you want it to be.
    API_VERSION = '1.0.0'
    API_BUILD = 'Orchid'
    API_HOST = '0.0.0.0' # The IP address to use for serving the API.
    API_PORT = 8000 # The port number to bind to for serving the API.
    BASE_ROUTE = f'/api/{API_GENERATION}' #! This is the most important out of everything.
    BASE_URL = f"http://{API_HOST}:{API_PORT}/{BASE_ROUTE}" # Mostly for internal API querying.
    RESPONSE_CODES = WebRequests.HttpResponseCodes
    PLUGINS_DIRECTORY = f"./plugins"
    CONFIG = {
        "tokens": {}, # The key-value pairs of this automatically sync depending on what's in the database.
        "database": { # The actual database server that houses all of the real data tables.
            "name": "my_database_here", # The MySQL database to connect to.
            "endpoint": "my_hostname_here", # Hostname it's located at, i.e. "my-db.xxxxxxxxx.us-east-1.rds.amazonaws.com"
            "username": "my_username_here", # The actual database (one defined above) username.
            "password": "my_password_here", # The actual database username password.
            "port": 3306 # Usually MySQL uses 3306, but you can use whatever you want.
        },
        "forwarding_server": { # Typically a server that you can login to with SSH and a terminal (proxy server).
            "hostname": "100.10.1.0", # Change with (most likely) the ip of the proxy server.
            "port": 22, # Usually going to be 22 for SSH/SFTP.
            "ssh_username": "my_username", # Actual SSH login of the user normally used.
            "ssh_key": "../my_key.pem", # .PEM files work the best with this variable.
            "local_address": "0.0.0.0", # Typically will be the loopback address or multi-loopback (0.0.0.0).
        },
        "plugins_directory": "./plugins" # Change this to wherever the actual plugins are located.
    }
    __db_name = CONFIG['database']['name']
    __db_host = CONFIG['database']['endpoint']
    __db_username = CONFIG['database']['username']
    __db_password = CONFIG['database']['password']
    __db_port = CONFIG['database']['port']
    __proxy_host = CONFIG['forwarding_server']['hostname']
    __proxy_port = CONFIG['forwarding_server']['port']
    __ssh_username = CONFIG['forwarding_server']['ssh_username']
    __ssh_key = CONFIG['forwarding_server']['ssh_key']
    __local_address = CONFIG['forwarding_server']['local_address']
    
    PRODUCTION_CONNECTION = f'mysql+pymysql://{__db_username}:{__db_password}@{__local_address}:[TUNNEL_PORT]/{__db_name}'
    DEVELOPMENT_CONNECTION = f"sqlite:///project.db"
    
    if DEBUG:
        DATABASE_URI = DEVELOPMENT_CONNECTION
    else:
        DATABASE_URI = PRODUCTION_CONNECTION
        PROXY_TUNNEL = SSHTunnelForwarder(
                (__proxy_host, __proxy_port),
                ssh_username=__ssh_username,
                ssh_pkey=__ssh_key,
                remote_bind_address=(__db_host, __db_port)
            )