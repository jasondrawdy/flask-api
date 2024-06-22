# flask-api

General framework for streamlining the creation process of Flask based micro-service APIs.

**Note**: This project was created using `Python 3.12.2`

## Features
- Containerized
- Advanced Logging
- Dynamic & modular
    - Automatically detects and registers the following (albeit manual `__init__.py` imports still being required):
        - Endpoints
        - Models
- Native plugin support
    - Completely asynchronous
    - Single plugin and entire directory loading supported
    - Atomic plugin loading (hot-reloading) for on-the-fly plugin updates
- Highly secure communications (internal & external)
    - Salted & Peppered passwords
    - SHA-512 hashing along with HMAC
    - Route (method) decorators to check for `admin_required`, `login_required`, `rate_limit` and `internal_only`
- Object Relational Mapping (ORM) ready
    - Uses MySQL for the core database technology
    - Allows connecting to either a local SQL instance (debug mode) or a production server
        - AWS/proxy ready

## Endpoints & Models
Pre-configured endpoints and models have been created to showcase possibility (no particular order here):
- Auth
    - Login *(endpoint)*
    - Logout *(endpoint)*
    - Register *(endpoint)*
    - Password Resets *(endpoint)*
- Carriers *(model)*
    - Products *(model)*
- Config
    - Tokens *(model) (used for secure internal API communicaton)*
- Network
    - Service Requests *(model) (tracks rate limits)*
- Roles *(model)*
    - Role Type *(model)*
    - Role Permissions *(model)*
    - Role Permission Type *(model)*
- Sessions *(endpoint)*
    - Create *(endpoint)*
    - Get *(endpoint)*
    - Delete *(endpoint)*
- Users *(endpoint)*
    - Create *(endpoint)*
    - Get *(endpoint)*
    - Update *(endpoint)*
    - Delete *(endpoint)*

**BONUS**: Testing *(endpoint) (rate limited to 10 per hour via the decorator and can be changed in `utils.decorators`)* 

## Installing Dependencies  
**NOTE**: The following dependencies will be installed on the current machine unless using a virtual environment.

1. Change directories into the main folder:  
`cd flask-api`

2. Install required dependencies:  
`pip3 install -r requirements.txt`  

## Starting the API with & without Docker
### With Docker
1. Build an image of the current source code to actually run with docker:  
`docker build --tag flask-api .`

2. Run the image with docker and expose the correct ports with the `-p` flag:  
*(Adding `-d` will allow you to run in "detached" mode so you can run the image in the background!)*  
`docker run -p 8000:8000 flask-api`  

3. Open a terminal use the following command to test that the API works (it should display a hash):  
`curl http://0.0.0.0:8000/api/v1/testing`

### Without Docker
1. Change into the source directory (if still in the main folder from installation):  
`cd src` 

2. Start or run the boilerplate microservice API:  
`python3 main.py`

3. Open a terminal use the following command to test that the API works (it should display a hash):  
`curl http://0.0.0.0:8000/api/v1/testing`  

**Note**: *The boilerplate service should now start a `werkzeug` debug server on `127.0.0.1:8000` (`0.0.0.0:8000`).  
It is a comprehensive WSGI web application library used only for debugging and **should not** be used in production.*  

**Tip**: *If on Linux or macOS, you can use the following command to stop, remove, and purge all images and containers at once:  
`docker ps -aq | xargs docker stop | xargs docker rm; docker image prune -a`*

<!-- ## To run Docker-compose:
Use the following command to start the service with docker-compose:  
`docker-compose -p flaskapi up -d`  -->

## Building Documentation
1. Change into the documentation directory (if still in the main folder from installation):  
`cd docs` 

2. Edit files as you see fit as well as files in `_templates` and `_static`.

2. Build the documentation for the entire project using:  
`sphinx-build -b html . _build`   
