from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException
from . import validat





#cart
class user():
    def create_user(self,db: Session, new_user: schemas.userCreate):
        v=validat.validate()
        v.check_user(user=new_user,db=db)

        user=models.User(busn_id=new_user.busn_id,owner_id=new_user.owner_id,serial=new_user.serial)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def search_user(self ,db:Session,busn_id:str, n_id:str,serial:str ):
        s_user=db.query(models.User).filter(( models.User.owner_id==n_id),(models.User.serial==serial),(models.User.busn_id == busn_id)).first()
        if(s_user):
            return s_user
        else:
            raise HTTPException(status_code=400,detail= "this User not exist in our system")      
    
    def get_user_by_serial(self,db:Session,serial:str):
        return db.query(models.User).filter(models.User.serial==serial).first()


    def get_user_by_busn_id(self,db:Session,busn_id:str):
        return db.query(models.User).filter(models.User.busn_id==busn_id).first()

    def get_user_by_n_id(self,db:Session,n_id:str):
        return db.query(models.User).filter(models.User.owner_id==n_id).first()

