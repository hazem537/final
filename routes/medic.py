from typing import List
from fastapi import Depends,APIRouter , HTTPException
from sqlalchemy.orm import Session
from sql_app import  models , schemas
from sql_app.database import get_db
from add import oauth
from sql_app.entity import medic as m


router = APIRouter()
medic = m.Medic()





@router.get("/medic/", response_model=schemas.Medic ,tags=["medic"])
def read_medic(medic_id:int, db: Session = Depends(get_db),curent_user=Depends(oauth.get_current_pharmacy_or_company)):
    med = medic.get_medic(db=db, medic_id=medic_id)
    return med

@router.get("/medic_like_name/", response_model=list[schemas.Medic] ,tags=["medic"])
def read_medic(medic_like_name:str, db: Session = Depends(get_db),curent_user=Depends(oauth.get_current_pharmacy_or_company)):
    med=medic.get_medic_like_name(db=db,medic_like_name=medic_like_name)
    return med
    

@router.get("/medics/", response_model=List[schemas.Medic],tags=["medic"])
def read_medics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),curent_user=Depends(oauth.get_current_pharmacy_or_company)):
    meds = medic.get_medics(db=db, skip=skip, limit=limit)
    return meds
@router.post("/medic/",tags=["medic"])
def create_medic(med: schemas.MedicCreate, db: Session = Depends(get_db),curent_user=Depends(oauth.get_current_company)):
    comp=curent_user
    db_med=medic.create_medic(db=db,new_medic=med,company_id=comp.id)    
    return db_med
@router.delete("/medic/{medic_id}",tags=['medic'])
def delete_medic(medic_id: int, db: Session = Depends(get_db), curent_user=  Depends(oauth.get_current_company) ):
    db_medic=medic.delete_medic(db=db,medic_id=medic_id)
    return db_medic
@router.put("/medic/{medic_id}" ,response_model=schemas.Medic,tags=['medic'])
def update_medic(medic_id:int,new_medic:schemas.MedicCreate,db:Session=Depends(get_db),curent_user= Depends(oauth.get_current_company)):
    db_medic=medic.update_medic(db=db,medic_id=medic_id,new_medic=new_medic)
    return db_medic    

