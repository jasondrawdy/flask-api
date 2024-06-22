from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime
from database import db

class ResetRequests(db.Model):
    __tablename__ = 'reset_requests'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, doc="Default primary key for the table.")
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, doc="The primary email of the user requesting a reset.")
    time_requested: Mapped[datetime] = mapped_column(DateTime, nullable=False, doc="The date and time of the original reset request.")
    time_resolved: Mapped[datetime] = mapped_column(DateTime, nullable=True, doc="The date and time of the request's resolution.")
    
    def get_id(self):
        """Return the primary key of the user object."""
        return self.id
    
    def as_dict(self: "ResetRequests"):
        """Converts the current database model into its JSON dictionary equivalent."""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}