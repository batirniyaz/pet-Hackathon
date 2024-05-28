from fastapi import FastAPI
from database import SessionLocal, engine
from models import Base
from routes import router as api_router


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(api_router)
