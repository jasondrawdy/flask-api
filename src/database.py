from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import force_auto_coercion
from loaders.models import load_models
from settings import Settings
from utils.logger import Logger
log = Logger(__name__)

__all__ = ('db', 'query', 'init_db') #? Specifically only export 'db' for public access.
db = SQLAlchemy() #? Our global DB object (imported by models & views & everything else).
query = db.session.query #? Support importing a functioning session query.

def init_db(app, db):
    """Initializes the global database object used by the app."""
    if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
        if not Settings.DEBUG: 
            Settings.PROXY_TUNNEL.start()
            tunnel_port = str(Settings.PROXY_TUNNEL.local_bind_port)
            Settings.DATABASE_URI = Settings.PRODUCTION_CONNECTION.replace("[TUNNEL_PORT]", tunnel_port)
            app.config["SQLALCHEMY_DATABASE_URI"] = Settings.DATABASE_URI
        force_auto_coercion()
        load_models()
        db.init_app(app)
        with app.app_context():
            log.success(f"CONNECTED TO ({Settings.DATABASE_URI}) — SYNCING TABLES!")
            db.create_all()
    else:
        raise ValueError('Cannot init DB without db and app objects.')
