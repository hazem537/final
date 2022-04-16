from typing import List
from fastapi import Depends,APIRouter 
from sql_app.entity import pharmacy as pha,company as comp ,auth 
from sql_app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import  OAuth2PasswordRequestForm
from add import oauth
router = APIRouter()
auth_pharmacy = pha.Pharmacy()
auth_company= comp.Company()


@router.post("/login/",tags=["auth"])
def read_pha(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    return auth.check_user_auth(db=db,email=form_data.username,password=form_data.password)


@router.get("/company_logout/",tags=["auth"])
def read_pha( db: Session = Depends(get_db),curent_user=Depends(oauth.get_current_company)):
    my_comp=curent_user
    return auth_company.log_out(db,my_comp.id)

@router.get("/pharmacy_logout/",tags=["auth"])
def read_pha( db: Session = Depends(get_db),curent_user=Depends(oauth.get_current_pharmacy)):
    my_pha=curent_user
    auth_pharmacy.log_out(db,my_pha.id)
    return "Done" 



