from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .. import models, schemas
from add import hash,token
from fastapi import HTTPException
from . import medic

h=hash.Hash()



#cart
class Cart():
    def create_cart(self,db: Session, new_cart: schemas.CartCreate,pharmacy_id:int):

        trans= self.check_cart(db=db, new_cart=new_cart, pharmacy_id=pharmacy_id) 
        if(trans== False):
            m= medic.Medic()
            comp_id=m.get_comp_id_of_medic(db, medic_id=new_cart.medic_id)
            db_cart = models.Cart(pharmacy_id=pharmacy_id,company_id=comp_id,medic_id=new_cart.medic_id,medic_amount=new_cart.medic_amount)
            db.add(db_cart)
            db.commit()
            db.refresh(db_cart)
            return db_cart
        else:
            return trans    

    def get_carts(self,db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Cart).offset(skip).limit(limit).all()

    def get_cart(self,db: Session, cart_id: int):
        return db.query(models.Cart).filter(models.Cart.id == cart_id).first()

    def check_cart(self,db: Session,new_cart:schemas.CartCreate,pharmacy_id:int):
      
        trans = db.query(models.Cart).filter(models.Cart.pharmacy_id == pharmacy_id  and models.Cart.medic_id== new_cart.medic_id ).first()
      
        if(trans):
          
            trans.medic_amount+=new_cart.medic_amount
            self.update_cart(db=db, cart_id=trans.id, new_cart=trans)
            return trans
        else:
            return False



    def get_cart_pha_id(self,db: Session, pharmacy_id: int):
        return db.query(models.Cart).filter(models.Cart.pharmacy_id == pharmacy_id).all()
    

    def delete_cart(self,db: Session, cart_id: int):  
        db_cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
        if db_cart:
            db.delete(db_cart)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="This Order is Not Exist")    
        return "deleted"  


    def delete_all_cart(self,db: Session, pharmacy_id: int):  
        db_cart = db.query(models.Cart).filter(models.Cart.pharmacy_id == pharmacy_id).all()
        for cart in db_cart :
            if cart:
                db.delete(cart)
                db.commit()
            else:
                raise HTTPException(status_code=404, detail="this pharmacy dont has no medic in her cart")    
        return "deleted"  

    def update_cart(self,db: Session, cart_id: int, new_cart: schemas.CartCreate):
        db_cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
        if db_cart:
            db_cart.pharmacy_id=new_cart.pharmacy_id
            db_cart.company_id=new_cart.company_id
            db_cart.medic_id=new_cart.medic_id
            db_cart.medic_amount=new_cart.medic_amount
            db.commit()
            db.refresh(db_cart)
        return db_cart  

 
