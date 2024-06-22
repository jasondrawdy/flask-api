from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, Column, Integer
from database import db

class RolePermissions(db.Model):
    __tablename__ = 'role_permissions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, doc="Default primary key for the table.")
    role_type_id: Mapped[int] = Column(Integer, ForeignKey('role_types.id'), nullable=False, doc="The id of the actual role type.")
    permission_type_id: Mapped[int] = Column(Integer, ForeignKey('role_permission_types.id'), nullable=False, doc="The id of the actual permission type.")
    
    def get_id(self):
        """Return the primary key of the user object."""
        return self.id
    
    def as_dict(self: "RolePermissions"):
        """Converts the current database model into its JSON dictionary equivalent."""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}