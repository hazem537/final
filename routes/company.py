from typing import List
from fastapi import Depends,APIRouter , HTTPException
from sqlalchemy.orm import Session
from sql_app import  models , schemas
from sql_app.entity import company as comp
from sql_app.database import get_db
from add.oauth import get_current_company 


router = APIRouter()
company= comp.Company()



@router.get("/company/", response_model=schemas.Company,tags=["Company"])
def read_company(company_id:int, db: Session = Depends(get_db),current_user=Depends(get_current_company)):
    comp = company.get_company(db=db,company_id=company_id)
    return comp

@router.get("/companys/", response_model=List[schemas.Company],tags=["Company"])
def read_companys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user=Depends(get_current_company)):
    comps = company.get_companys(db=db, skip=skip, limit=limit)
    return comps
@router.post("/company/",response_model=schemas.comp_with_token,tags=["Company"])
def create_company(comp: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_comp=company.create_company(db=db,new_comp=comp)    
    return db_comp
@router.delete("/company/{company_id}",tags=['Company'])
def delete_coompany(company_id: int, db: Session = Depends(get_db),curent_user= Depends(get_current_company)):
    db_comp=company.delete_company(db=db,company_id=company_id)
    return db_comp
@router.put("/company/{company_id}" ,response_model=schemas.Company,tags=['Company'])
def update_company(company_id:int,new_company:schemas.CompanyCreate,db:Session=Depends(get_db),curent_user= Depends(get_current_company)):
    db_comp=company.update_company(db=db,company_id=company_id,new_company=new_company)
    return db_comp