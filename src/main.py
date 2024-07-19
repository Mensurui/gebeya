from .data.dependency import init_db, get_db
from fastapi import FastAPI, Depends
from .model import model
from sqlalchemy.ext.asyncio import AsyncSession
from .web import endpoint
from .service import auth
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root(db:AsyncSession=Depends(get_db)):
    return {"gebeya"}

app.include_router(endpoint.router)
app.include_router(auth.router)
