from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from database import db

class RoleTypes(db.Model):
    __tablename__ = 'role_types'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, doc="Default primary key for the table.")
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False, doc="The actual name of the role.")
    description: Mapped[str] = mapped_column(String, nullable=True, doc="A long description of the actual role.")
    permissions = db.relationship('RolePermissions', backref='role_type', lazy=True, doc="Available ways to access resources for the role.")
    
    def get_id(self):
        """Return the primary key of the user object."""
        return self.id
    
    def as_dict(self: "RoleTypes"):
        """Converts the current database model into its JSON dictionary equivalent."""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}