from typing import List
from fastapi import Depends, APIRouter, HTTPException, Body
from sqlalchemy.orm import Session
from sql_app import models, schemas
from sql_app.database import get_db
from add import oauth
from sql_app.entity import pharmacy as pha


router = APIRouter()
pharmacy = pha.Pharmacy()


@router.get("/pharmacy/me", response_model=schemas.Pharmacy, tags=['pharmacy'])
def read_pharmacy(db: Session = Depends(get_db), curent_user=Depends(oauth.get_current_pharmacy)):
    my_pha = curent_user
    pha = pharmacy.get_pharmacy(db=db, pharmacy_id=my_pha.id)
    return pha


@router.get("/near_pharmacys/",  tags=['pharmacy'])
def read_pharmacys(db: Session = Depends(get_db),curent_user=Depends(oauth.get_current_pharmacy)):
    mypharmacy=curent_user
    result  =pharmacy.get_near_pharmacys(db,mypharmacy.govern, mypharmacycity) 
    return result


@router.post("/pharmacy/", response_model=schemas.pha_with_token, tags=['pharmacy'])
def create_pharmacy(pha: schemas.PharmacyCreate, db: Session = Depends(get_db)):
    db_pha = pharmacy.create_pharmacy(db=db, new_Pha=pha)
    return db_pha


@router.delete("/pharmacy/", tags=['pharmacy'])
def delete_pharmacy(db: Session = Depends(get_db), curent_user=Depends(oauth.get_current_pharmacy)):
    my_pha = curent_user
    db_pha = pharmacy.delete_Pharmacy(db=db, pharmacy_id=my_pha.id)
    return db_pha


@router.put("/pharmacy/", response_model=schemas.Pharmacy, tags=['pharmacy'])
def update_pharmacy(new_pharmacy: schemas.PharmacyCreate, db: Session = Depends(get_db), curent_user=Depends(oauth.get_current_pharmacy)):
    my_pha = curent_user
    db_pha = pharmacy.update_pharmacy(
        db=db, pharmacy_id=my_pha.id, new_pharmacy=new_pharmacy)
    return db_pha
