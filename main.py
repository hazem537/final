from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from sql_app import models, schemas
from sql_app.database import SessionLocal, engine

from routes import pharmacy, company, cart, order, medic, auth,user




app = FastAPI()

models.Base.metadata.create_all(bind=engine)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(pharmacy.router)
app.include_router(company.router)
app.include_router(medic.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(auth.router)
app.include_router(user.router)
