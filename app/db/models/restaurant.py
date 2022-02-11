"""Restaurant structure for the DB"""
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from db.base import Base


class Restaurant(Base):
    """Model for SQLAlchemy for the restaurant Table in the DB"""

    __tablename__ = "restaurant"

    place_id = Column(String, primary_key=True)
    name = Column(String, nullable=False, autoincrement=False)

    bewertungen = relationship("Bewertung", back_populates="restaurant", passive_deletes=True)
