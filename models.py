from sqlalchemy import String, Integer, Column
from database import Base

class proyecto(Base):
        __tablename__ = "proyectos"
        id = Column(Integer, primary_key=True, index=True)
        title = Column(String)
        description = Column(String)
        image = Column(String)
        urlRepository = Column(String)
        urlDemo = Column(String)