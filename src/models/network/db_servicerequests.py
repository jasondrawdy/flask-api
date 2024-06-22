from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from database import db, query

class ServiceRequests(db.Model):
    __tablename__ = 'service_requests'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, doc="Default primary key for the table.")
    user_id: Mapped[str] = Column(Integer, ForeignKey('users.id'), nullable=True, doc="The user that made the request, if available.")
    request_ip: Mapped[str] = mapped_column(String, nullable=False, doc="The original ip of the request sender.")
    request_origin: Mapped[str] = mapped_column(String, nullable=True, doc="The origin of the request, if available..")
    request_destination: Mapped[str] = mapped_column(String, nullable=False, doc="The destination of the request.")
    created_on: Mapped[datetime] = mapped_column(DateTime, nullable=False, doc="Time and date the request was sent.")
    
    def get_id(self):
        """Return the primary key of the service request object."""
        return self.id
    
    def as_dict(self: "ServiceRequests"):
        """Converts the current database model into its JSON dictionary equivalent."""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}