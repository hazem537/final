from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .. import models, schemas
from add import hash,token
from fastapi import HTTPException
from . import validat,create_code,pharmacy

h=hash.Hash()

class Company():
    def create_company(self,db: Session, new_comp: schemas.CompanyCreate):
        
        v=validat.validate()
        v.check_company(company=new_comp ,db=db)
        new_comp.password=h.hashing_password(new_comp.password)

        db_comp = models.Company(
            email=new_comp.email,
            password=new_comp.password,
            username=new_comp.username,
            serial=new_comp.serial,
            owner_id=new_comp.owner_id,
            comp_id=new_comp.comp_id,
            phone_number=new_comp.phone_number,
            govern=new_comp.govern,
            city=new_comp.city,
            street=new_comp.street,
            active=True,
            authorized=False,
            authorized_code=create_code.get_auth_code()
            )
        db.add(db_comp)
        db.commit()
        db.refresh(db_comp)
        tok=token.tok()
        access_token_expires = timedelta(minutes=tok.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token =tok.create_access_token(
        data={"sub": f"{db_comp.id}$company"}, expires_delta=access_token_expires)
        result= schemas.comp_with_token(
            access_token=access_token,
            token_type="bearer",
            comp=db_comp,
            type="company"
        )
        return result
        

    def get_companys(self,db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Company).offset(skip).limit(limit).all()
    def get_company(self,db: Session, company_id: int):
        return db.query(models.Company).filter(models.Company.id == company_id).first()
    def get_company_by_phoen_number(self,db: Session, phone_number: str):
        return db.query(models.Company).filter(models.Company.phone_number == phone_number).first()
 

    def get_company_by_serial(self,db: Session, serial: str):
            return db.query(models.Company).filter(models.Company.serial == serial).first()
    def get_company_by_email(self,db: Session, email: str):
        return db.query(models.Company).filter(models.Company.email == email).first()
    def get_company_by_owner_id(self,db: Session, owner_id: str):
        return db.query(models.Company).filter(models.Company.owner_id == owner_id).first()
    def get_company_by_comp_id(self,db: Session, comp_id: str):
            return db.query(models.Company).filter(models.Company.comp_id == comp_id).first()
          



    def check_company(self,db:Session, email:str,password:str):
        #----------- strart validation 
        v=validat.validate()
        v.is_log_valid_email(email)
        db_comp=db.query(models.Company).filter(models.Company.email == email).first()
        if(db_comp == None):
            #eror we dont have pharmacy with that username
            raise HTTPException(status_code=404,detail="Ther is no account with this Email ")
            
        #---------------end validation

        if(h.verify_password(plain_password=password,hashed_password=db_comp.password) == True):
            #here you can acces your data
            tok=token.tok()
            access_token_expires = timedelta(minutes=tok.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token =tok.create_access_token(
            data={"sub": f"{db_comp.id}$company"}, expires_delta=access_token_expires)
            self.update_company_online(db=db,company_id=db_comp.id)
            return {"access_token": access_token, "token_type": "bearer","type":"company","company":db_comp}
        else:
            raise HTTPException(status_code=400,detail="Wrong Password  Try again")
            #here we have eror that is wrong password
            pass   


    def delete_company(self,db: Session, company_id: int):  
        db_comp = db.query(models.Company).filter(models.Company.id == company_id).first()
        if db_comp:
            db.delete(db_comp)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="This Pharmacy Not Exist")    
        return None  

    def update_company(self,db: Session, company_id: int, new_company: schemas.CompanyCreate):
        db_comp = db.query(models.Company).filter(models.Company.id == company_id).first()
        if db_comp:
            db_comp.username=new_company.username
            db_comp.email=new_company.email
            db_comp.password=h.hashing_password(new_company.password)
            db_comp.serial=new_company.serial
            db_comp.phone_number=new_company.phone_number
            db_comp.location=new_company.location
            db.commit()
            db.refresh(db_comp)
        return db_comp   

    def update_company_online(self,db: Session, company_id: int):
        db_comp = db.query(models.Company).filter(models.Company.id == company_id).first()
        if db_comp:
            db_comp.active=True
            db.commit()
            db.refresh(db_comp)
        return db_comp  

    def log_out(self,db:Session,company_id:int):
        db_comp= self.get_company(db=db,company_id=company_id)
        if(db_comp):
            db_comp.active=False
            db.commit()
            db.refresh(db_comp)
        return db_comp    
