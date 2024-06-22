from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from database import db

class Sessions(db.Model):
    __tablename__ = 'sessions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, doc="Default primary key for the table.")
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False, doc="The user that started the session.")
    started_on: Mapped[datetime] = mapped_column(DateTime, nullable=False, doc="Date and time the session was created.")
    expires_on: Mapped[datetime] = mapped_column(DateTime, nullable=False, doc="Date and time the session expires.")
    original_signature: Mapped[str] = mapped_column(String, unique=True, nullable=False, doc="The original session signature that was created.")
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False, doc="A uniquely generated session identifier.")
    ip: Mapped[str] = mapped_column(String, nullable=False, doc="The original IP that created the session.")
    
    def get_id(self):
        """Return the primary key of the user object."""
        return self.id
    
    def as_dict(self: "Sessions"):
        """Converts the current database model into its JSON dictionary equivalent."""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}