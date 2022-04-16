from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .. import models, schemas
from add import hash,token
from fastapi import HTTPException
from .import pharmacy,company

pha=pharmacy.Pharmacy()
comp=company.Company()
h=hash.Hash()

def check_user_auth(db:Session,email:str,password:str):
    pha_db=pha.get_pharmacy_by_email(db=db,email=email)
    comp_db=comp.get_company_by_email(db=db,email=email)
    if(pha_db):
        return pha.check_pharmacy(db=db,email=email,password=password)
    elif(comp_db):
        return comp.check_company(db=db,email=email,password=password) 
    else:
        raise HTTPException(status_code=404, detail="this email not exist")    
