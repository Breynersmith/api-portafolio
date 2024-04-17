from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import os
import uvicorn

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



PORT = int(os.environ.get("PORT", 8000))
HOST = '0.0.0.0'

@app.post("/nuevo-proyecto", status_code=status.HTTP_201_CREATED)
async def agregar_proyecto(proyecto: Proyecto, db:db_dependency):
        try:
                nuevo_proyecto =  models.proyecto(**proyecto.dict())
                db.add(nuevo_proyecto)
                db.commit()
                return "se agrego el proyecto correctamente"
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/proyectos")
async def obtener_proyectos(db:db_dependency):
        try:
                proyectos = db.query(models.proyecto).all()
                return proyectos
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
@app.get("/")
async def root():
        return {"message": "bienvenido a mi api FastAPI"}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=os.getenv("PORT", 10000))