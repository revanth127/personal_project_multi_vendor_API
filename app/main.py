from fastapi import FastAPI
from app.database import engine
from app.database import Base
import app.models as models
from app.routers import auth,users


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

