from typing import List
from fastapi import Depends,APIRouter , HTTPException
from sqlalchemy.orm import Session
from sql_app import  models , schemas
from sql_app.entity import cart as c
from sql_app.database import get_db
from add import oauth


router = APIRouter()

cart=c.Cart()


#@router.get("/cart/", response_model=schemas.Cart,tags=["cart"])
#def read_cart(cart_id:int, db: Session = Depends(get_db),curent_user= Depends(oauth.get_current_pharmacy)):
#    s_cart = cart.get_cart(db=db,cart_id=cart_id)
#   return s_cart

# get my cart
@router.get("/mycart/", response_model=list[schemas.Cart],tags=["cart"])
def read_cart( db: Session = Depends(get_db),curent_user= Depends(oauth.get_current_pharmacy)):
    pharmacy=curent_user
    pharm_cart=cart.get_cart_pha_id(db=db,pharmacy_id=pharmacy.id )
    return pharm_cart

#
#@router.get("/carts/", response_model=List[schemas.Cart],tags=["cart"])
#def read_carts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),curent_user= Depends(oauth.get_current_pharmacy)):
#    s_carts = cart.get_carts(db=db, skip=skip, limit=limit)
#    return s_carts



# add anew cart 
@router.post("/cart/", response_model=schemas.Cart,tags=["cart"])
def create_cart(new_cart: schemas.CartCreate, db: Session = Depends(get_db),curent_user= Depends(oauth.get_current_pharmacy)):    
    pharmacy=curent_user
    db_cart=cart.create_cart(db=db,new_cart=new_cart,pharmacy_id=pharmacy.id)    
    return db_cart

# delete cart 
@router.delete("/cart/{cart_id}",tags=['cart'])
def delete_cart(cart_id: int, db: Session = Depends(get_db),curent_user= Depends(oauth.get_current_pharmacy)):
    db_cart=cart.delete_cart(db=db,cart_id=cart_id)
    return db_cart

@router.delete("/deleteAllCart/",tags=['cart'])
def delete_cart( db: Session = Depends(get_db),curent_user= Depends(oauth.get_current_pharmacy)):
    pharmacy=curent_user
    db_cart=cart.delete_all_cart(db=db,pharmacy_id=pharmacy.id)
    return db_cart
   

#update cart    
@router.put("/cart/{cart_id}" ,response_model=schemas.Cart,tags=['cart'])
def update_cart(cart_id:int,new_cart:schemas.CartCreate,db:Session=Depends(get_db),curent_user= Depends(oauth.get_current_pharmacy)):
    db_cart=cart.update_cart(db=db,cart_id=cart_id,new_cart=new_cart)
    return db_cart