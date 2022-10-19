from fastapi import FastAPI

from src.models.db import database, User

app = FastAPI(title="Lottery-sys")


@app.get("/")
async def read_root():
    return await User.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    await User.objects.get_or_create(username="test")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
