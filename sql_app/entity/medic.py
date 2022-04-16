from sqlalchemy.orm import Session
from sqlalchemy import func 
from datetime import datetime, timedelta
from ..import models, schemas
from add import hash,token
from fastapi import HTTPException
from. import validat 

h=hash.Hash()

class Medic():

    def create_medic(self,db: Session, new_medic: schemas.MedicCreate,company_id:int):

        v=validat.validate()
                    

        db_medic = models.Medic(
            name=new_medic.name,
            price=new_medic.price,
            active_substance=new_medic.active_substance,
            stock =new_medic.stock ,
            company_id=company_id
            )
        v.check_medic(medic=new_medic,comp_id=company_id,db=db) 
        db.add(db_medic)
        db.commit()
        db.refresh(db_medic)
        return db_medic

    def get_medics(self,db: Session):
        return db.query(models.Medic).all()
        
    def check_medic(self,db: Session, medic: schemas.MedicCreate,comp_id:int):
        return db.query(models.Medic).filter((func.lower( models.Medic.name)== medic.name.lower()),(func.lower(models.Medic.active_substance) == medic.active_substance),(models.Medic.company_id == comp_id)).first()

    def get_medic(self,db: Session, medic_id: int):
        return db.query(models.Medic).filter(models.Medic.id == medic_id).first()


    def get_comp_id_of_medic(self,db: Session, medic_id: int):
        return db.query(models.Medic).filter(models.Medic.id == medic_id).first().company_id



    def get_medic_like_name(self,db: Session, medic_like_name: str):
        print(medic_like_name)
        medics= db.query(models.Medic).filter(models.Medic.name.like(f"%{medic_like_name}%")).all()
        print(medics)
        return medics


    def delete_medic(self,db: Session, medic_id: int):  
        db_medic = db.query(models.Medic).filter(models.Medic.id == medic_id).first()
        if db_medic:
            db.delete(db_medic)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="This Order is Not Exist")    
        return None  

    def update_medic(self,db: Session, medic_id: int, new_medic: schemas.MedicCreate):
        db_medic = db.query(models.Medic).filter(models.Medic.id == medic_id).first()
        if db_medic:
            db_medic.name=new_medic.name
            db_medic.price=new_medic.price
            db_medic.active_substance=new_medic.active_substance
            db_medic.company_id=new_medic.company_id

            db.commit()
            db.refresh(db_medic)
        return db_medic  

    def update_medic_stock(self,db: Session, medic_id: int, order_amount:int):
        db_medic = db.query(models.Medic).filter(models.Medic.id == medic_id).first()
        if db_medic:
            db_medic.stock=db_medic.stock-order_amount
            db.commit()
            db.refresh(db_medic)
        return db_medic  


