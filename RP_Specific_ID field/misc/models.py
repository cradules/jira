from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(String, index=True)
    issue_id = Column(String, unique=True, index=True)
    issue_type = Column(String, index=True)
    package = Column(String, index=True, nullable=True)
    linked_issues = Column(String, index=True, nullable=True)
