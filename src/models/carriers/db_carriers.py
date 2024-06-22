from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from database import db

class Carriers(db.Model):
    __tablename__ = 'carriers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, doc="Default primary key for the table.")
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False, doc="The actual name of the carrier.")
    
    def get_id(self):
        """Return the primary key of the user object."""
        return self.id
    
    def as_dict(self: "Carriers"):
        """Converts the current database model into its JSON dictionary equivalent."""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}