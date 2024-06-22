from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from database import db

class Users(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, doc="Default primary key for the table.")
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, doc="The chosen username of the user.")
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False, doc="The hashed password for the provided username.")
    salt: Mapped[str] = mapped_column(String, unique=True, nullable=True, doc="Salt used to make the password unique.")
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, doc="The primary email of the user.")
    first_name: Mapped[str] = mapped_column(String, nullable=False, doc="The legal first name of the user.")
    last_name: Mapped[str] = mapped_column(String, nullable=False, doc="The legal last name of the user.")
    created_on: Mapped[datetime] = mapped_column(DateTime, unique=False, nullable=False, doc="Time and date the user was first created.")
    updated_on: Mapped[datetime] = mapped_column(DateTime, unique=False, nullable=True, doc="Time and date the user was last updated.")
    last_login: Mapped[str] = mapped_column(String, unique=False, nullable=True, doc="Time and date the user last logged in.")
    admin: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False, doc="A flag determining if the user is an administrator.")
    authenticated: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False, doc="A flag determining if the user is authenticated.")
    sessions = db.relationship('Sessions', backref='user', lazy=True)
    roles = db.relationship('Roles', backref='user', lazy=True)
    
    def get_id(self):
        """Return the primary key of the user object."""
        return self.id
    
    def is_active(self):
        """True, as all users are active."""
        return True

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_admin(self):
        """Return True if the user is an admin; aka, 'God mode'."""
        return self.admin
    
    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    def as_dict(self: "Users"):
        """Converts the current database model into its JSON dictionary equivalent."""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    
    def for_web(self: "Users"):
        """Returns an object used for a successful login."""
        user = {
            "user_id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
        return user