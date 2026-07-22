from fastapi import FastAPI
from routers import users

from crud.database import init_db

app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()


app.include_router(users.router)


@app.get("/")
def hello():
    return {"message": "Flight Booking Api"}
