from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.post("/nuevo-proyecto", status_code=status.HTTP_201_CREATED)
async def agregar_proyecto(proyecto: Proyecto, db:db_dependency):
        try:
                nuevo_proyecto =  models.proyecto(**proyecto.dict())
                db.add(nuevo_proyecto)
                db.commit()
                return "se agrego el proyecto correctamente"
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

PORT = int(os.environ.get("PORT", 8000))
HOST = '0.0.0.0'

if __name__ == "__main__":
    uvicorn.run('main:app', host= HOST, port= PORT, reload=True)