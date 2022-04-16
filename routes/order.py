from typing import List
from fastapi import Depends,APIRouter , HTTPException
from sqlalchemy.orm import Session
from sql_app import  models , schemas
from sql_app.database import get_db
from add import oauth
from sql_app.entity import order as o



router = APIRouter()
order= o.Order()

@router.get("/order/", response_model=schemas.Order,tags=["order"])
def read_order(order_id:int, db: Session = Depends(get_db),curent_user=  Depends(oauth.get_current_pharmacy_or_company)):
    s_order = order.get_order(db=db, order_id=order_id)
    return s_order

@router.get("/orders/", response_model=List[schemas.Order],tags=["order"])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),curent_user=  Depends(oauth.get_current_pharmacy_or_company)):
    s_orders = order.get_orders(db=db, skip=skip, limit=limit)
    return s_orders

@router.post("/order/", response_model=schemas.Order ,tags=["order"])
def create_order(cart_id:int, db: Session = Depends(get_db),curent_user=  Depends(oauth.get_current_pharmacy_or_company)):
    db_order=order.create_order(db=db,cart_id=cart_id)    
    return db_order

@router.delete("/order/{order_id}",tags=['order'])
def delete_order(order_id: int, db: Session = Depends(get_db), curent_user=  Depends(oauth.get_current_pharmacy_or_company) ):
    db_order=order.delete_order(db=db,order_id=order_id)
    return db_order
@router.put("/order/{order_id}" ,response_model=schemas.Order,tags=['order'])
def update_order(order_id:int,new_order:schemas.OrderCreate,db:Session=Depends(get_db),curent_user= Depends(oauth.get_current_pharmacy_or_company)):
    db_order=order.update_order(db=db,order_id=order_id,new_order=new_order)
    return db_order
