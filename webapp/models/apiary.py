from sqlalchemy import Column, String, Integer

from webapp.database import Base


class Apiary(Base):
    __tablename__ = 'apiary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __repr__(self):
        return f"<Apiary(id={self.id}, " \
               f"name={self.name})>"
