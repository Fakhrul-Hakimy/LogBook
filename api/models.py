from sqlalchemy import Boolean, Column , ForeignKey , Integer ,String
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True , index=True)
    username = Column(String)
    password = Column(String)


class logs(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True , index=True)
    date = Column(String)
    time_in = Column(String)
    time_out = Column(String)
    comment = Column(String)
    image_path = Column(String)


