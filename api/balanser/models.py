from datetime import datetime


from sqlalchemy import (Column, Integer, String, Table)

from api.database import Base, metadata

class OriginServer(Base):
    __tablename__ = "origin_server"
    id = Column(Integer())
    url_server = Column(String())

