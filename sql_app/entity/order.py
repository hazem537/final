from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .. import models, schemas
from add import hash,token
from fastapi import HTTPException
from . import cart,medic

h=hash.Hash()

class Order():
    def create_order(self,db: Session, cart_id: int):
        c=cart.Cart()
        n_c=c.get_cart(db=db,cart_id=cart_id)
        if(n_c.medic_amount<= n_c.medic.stock ):
            m=medic.Medic()
            m.update_medic_stock(db=db,medic_id=n_c.medic_id,order_amount=n_c.medic_amount)
            db_order = models.Order(pharmacy_id=n_c.pharmacy_id,company_id=n_c.company_id,medic_id=n_c.medic_id,medic_amount=n_c.medic_amount,total=(n_c.medic_amount*n_c.medic.price),status="pending")
            db.add(db_order)
            db.commit()
            db.refresh(db_order)
            return db_order
        else:
            raise HTTPException(status_code=400 , detail= "stock is lower than your order " )

    def get_orders(self,db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Order).offset(skip).limit(limit).all()
    def get_order(self,db: Session, order_id: int):
        return db.query(models.Order).filter(models.Order.id == order_id).first()

    def delete_order(self,db: Session, order_id: int):  
        db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if db_order:
            db.delete(db_order)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="This Order is Not Exist")    
        return None  

    def update_order(self,db: Session, order_id: int, new_order: schemas.OrderCreate):
        db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if db_order:
            db_order.pharmacy_id=new_order.pharmacy_id
            db_order.company_id=new_order.company_id
            db_order.medic_id=new_order.medic_id
            db_order.medic_amount=new_order.medic_amount
            db_order.total=new_order.total
            db_order.status=new_order.status
            db.commit()
            db.refresh(db_order)
        return db_order  
