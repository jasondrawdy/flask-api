from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from database import db

class RolePermissionTypes(db.Model):
    __tablename__ = 'role_permission_types'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, doc="Default primary key for the table.")
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False, doc="The actual name of the permission type.")
    description: Mapped[str] = mapped_column(String, nullable=True, doc="A long description of the actual permission type.")
    
    def get_id(self):
        """Return the primary key of the user object."""
        return self.id
    
    def as_dict(self: "RolePermissionTypes"):
        """Converts the current database model into its JSON dictionary equivalent."""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}