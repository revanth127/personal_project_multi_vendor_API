from fastapi import APIRouter,FastAPI
from app.database import engine
from app.database import Base
import app.models as models


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

