from typing import List
from fastapi import Depends,APIRouter , HTTPException
from sqlalchemy.orm import Session
from sql_app import  models , schemas
from sql_app.database import get_db
from add import oauth
from sql_app.entity import dumy as d


router = APIRouter()
user = d.user()






@router.post("/user/",tags=["users"])
def create_user(new_user: schemas.userCreate, db: Session = Depends(get_db)):
    
    db_user=user.create_user(db=db,new_user=new_user)    
    return db_user
