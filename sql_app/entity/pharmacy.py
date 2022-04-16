from sqlalchemy.orm import Session
from datetime import  timedelta
from .. import models, schemas
from add import hash, token
from fastapi import HTTPException
from . import validat, create_code

h = hash.Hash()


class Pharmacy():
    def create_pharmacy(self, db: Session, new_Pha: schemas.PharmacyCreate):
        v=validat.validate()
        v.check_pharamcy(new_Pha,db)
        # start create new pharmcyn
        new_Pha.password = h.hashing_password(new_Pha.password)

        db_pha = models.Pharmacy(
            email=new_Pha.email,
            password=new_Pha.password,
            username=new_Pha.username,
            serial=new_Pha.serial,
            pha_id=new_Pha.pha_id,
            owner_id=new_Pha.owner_id,
            phone_number=new_Pha.phone_number,
            govern=new_Pha.govern,
            city=new_Pha.city,
            street=new_Pha.street,
            active=True,
            authorized=False,
            authorized_code=create_code.get_auth_code()
        )
        db.add(db_pha)
        db.commit()
        db.refresh(db_pha)
        # end create new pharmacy

        # start makeing token
        tok = token.tok()
        access_token_expires = timedelta(
            minutes=tok.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = tok.create_access_token(
            data={"sub": f"{db_pha.id}$pharmacy"}, expires_delta=access_token_expires)
        # end making token\
        result = schemas.pha_with_token(
            access_token=access_token,
            token_type="Bearer",
            pha=db_pha,
            type="pharmacy"
        )

        return result

    def get_near_pharmacys(self, db: Session, govern: str, city: str):
        result = []
        near_govern = db.query(models.Pharmacy).filter(
            models.Pharmacy.govern == govern).all()
        near_city = db.query(models.Pharmacy).filter(
            models.Pharmacy.city == city).all()
        result.extend(near_city)
        result.extend(near_govern)
        result = set(result)

        return result

    def get_pharmacys(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Pharmacy).offset(skip).limit(limit).all()

    def get_pharmacy(self, pharmacy_id: int, db: Session):
        return db.query(models.Pharmacy).filter(models.Pharmacy.id == pharmacy_id).first()

    def get_pharmacy_by_phone_number(self, phone_number:str, db: Session):
        return db.query(models.Pharmacy).filter(models.Pharmacy.phone_number == phone_number).first()


    def get_pharmacy_by_username(self, db: Session, username: str):
        return db.query(models.Pharmacy).filter(models.Pharmacy.username == username).first()

    def get_pharmacy_by_serial(self, db: Session, serial: str):
        return db.query(models.Pharmacy).filter(models.Pharmacy.serial == serial).first()

    def get_pharmacy_by_email(self, db: Session, email: str):
        return db.query(models.Pharmacy).filter(models.Pharmacy.email == email).first()

    def get_pharmacy_by_owner_id(self, db: Session, owner_id: str):
        return db.query(models.Pharmacy).filter(models.Pharmacy.owner_id == owner_id).first()

    def get_pharmacy_by_pha_id(self, db: Session, pha_id: str):
        return db.query(models.Pharmacy).filter(models.Pharmacy.pha_id == pha_id).first()

    def check_pharmacy(self, db: Session, email: str, password: str):
        v=validat.validate()
        v.is_log_valid_email(email)
        tok = token.tok()
        db_pha = db.query(models.Pharmacy).filter(
            models.Pharmacy.email == email).first()
        if(db_pha == None):
            # eror we dont have pharmacy with that username
            raise HTTPException(
                status_code=404, detail=" NO pharmacy with this Email")
        if(h.verify_password(plain_password=password, hashed_password=db_pha.password) == True):
            # here you can acces your data
            # return  db_pha
            access_token_expires = timedelta(
                minutes=tok.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = tok.create_access_token(
                data={"sub": f"{db_pha.id}$pharmacy"}, expires_delta=access_token_expires)
            self.update_pharmcy_online(db=db, pharmacy_id=db_pha.id)
            return {"access_token": access_token, "token_type": "bearer", "type": "pharmacy", "pharmacy": db_pha}
        else:
            raise HTTPException(
                status_code=400, detail=" this is wrong password")
            # here we have eror that is wrong password

    def delete_Pharmacy(self, db: Session, pharmacy_id: int):
        db_pha = db.query(models.Pharmacy).filter(
            models.Pharmacy.id == pharmacy_id).first()
        if db_pha:
            db.delete(db_pha)
            db.commit()
        else:
            raise HTTPException(
                status_code=404, detail="This Pharmacy Not Exist")
        return None

    def update_pharmacy(self, db: Session, pharmacy_id: int, new_pharmacy: schemas.PharmacyCreate):
        db_phar = db.query(models.Pharmacy).filter(
            models.Pharmacy.id == pharmacy_id).first()
        if db_phar:
            db_phar.username = new_pharmacy.username
            db_phar.email = new_pharmacy.email
            db_phar.password = h.hashing_password(new_pharmacy.password)
            db_phar.serial = new_pharmacy.serial
            db_phar.phone_number = new_pharmacy.phone_number
            db_phar.location = new_pharmacy.location
            db.commit()
            db.refresh(db_phar)
        return db_phar

    def update_pharmcy_online(self, db: Session, pharmacy_id: int):
        db_phar = db.query(models.Pharmacy).filter(
            models.Pharmacy.id == pharmacy_id).first()
        if db_phar:
            db_phar.active = True
            db.commit()
            db.refresh(db_phar)
        return db_phar

    def log_out(self, db: Session, pharmacy_id: int):
        db_pha = self.get_pharmacy(db=db, pharmacy_id=pharmacy_id)
        if(db_pha):
            db_pha.active = False
            db.commit()
            db.refresh(db_pha)
        return db_pha
