from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Column, ForeignKey
from database import db

class Roles(db.Model):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, doc="Default primary key for the table.")
    user_id: Mapped[str] = Column(Integer, ForeignKey('users.id'), nullable=False, doc="The main id of the user associated with the role.")
    role_type_id: Mapped[str] = Column(Integer, ForeignKey('role_types.id'), nullable=False, doc="The role id of the actual associated user role.")
    
    def get_id(self):
        """Return the primary key of the user object."""
        return self.id
    
    def as_dict(self: "Roles"):
        """Converts the current database model into its JSON dictionary equivalent."""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}