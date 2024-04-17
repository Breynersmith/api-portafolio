from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
app = FastAPI()

class Proyecto(BaseModel):
        title: str
        description: str
        image: str
        urlRepository: str
        urlDemo: str

def get_db():
        db = SessionLocal()
        try:
                yield db
        finally:
                db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/nuevo-proyecto", status_code=status.HTTP_201_CREATED)
async def agregar_proyecto(proyecto: Proyecto, db:db_dependency):
        try:
                nuevo_proyecto =  models.proyecto(**proyecto.dict())
                db.add(nuevo_proyecto)
                db.commit()
                return "se agrego el proyecto correctamente"
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

