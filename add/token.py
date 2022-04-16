from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from sql_app import schemas
from sql_app.entity import pharmacy as pha,company as comp







SECRET_KEY = "3656bb6c8c622f5f82478e6a65670c80fdb41d8cf2e821f593a55e25d7443f58"
ALGORITHM = "HS256"


class tok(): 
   ACCESS_TOKEN_EXPIRE_MINUTES = 24*60 # day 
   def create_access_token(self,data: dict, expires_delta: Optional[timedelta] = None):
      to_encode = data.copy()
      if expires_delta:
         expire = datetime.utcnow() + expires_delta
      else:
           expire = datetime.utcnow() + timedelta(minutes=15)
      to_encode.update({"exp": expire})
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
      return encoded_jwt

   def verify_token_pha_or_comp(self,token:str,credentials_exception,db):
      try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         phadata= payload.get("sub")
         user_id=phadata.rsplit("$")[0]
         user_type=phadata.rsplit("$")[1]
         if user_id == None :
                 raise credentials_exception
         token_data = schemas.TokenData(id=user_id,type=user_type)
      except JWTError:
            raise credentials_exception
      if(user_type == "pharmacy"):
            # login as pharmacy
            pharmacy=pha.Pharmacy()
            pharm=pharmacy.get_pharmacy(db=db,pharmacy_id=int(token_data.id))   
            if pharm == None:
               raise credentials_exception
            return pharm   
      elif(user_type == "company") :
            # login as copany
            company=comp.Company()
            compa=company.get_company(db=db,company_id=int(token_data.id))   
            if compa == None:
               raise credentials_exception
            return compa

        


   def verify_token_pha(self,token:str,credentials_exception,db):
      try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         phadata= payload.get("sub")
         user_id=phadata.rsplit("$")[0]
         user_type=phadata.rsplit("$")[1]
         if user_id == None or user_type == "company" :
             raise credentials_exception
         token_data = schemas.TokenData(id=user_id,type=user_type)
      except JWTError:
           raise credentials_exception
      pharmacy=pha.Pharmacy()
      pharm=pharmacy.get_pharmacy(db=db,pharmacy_id=int(token_data.id))   
      if pharm == None:
            raise credentials_exception
      return pharm

   def verify_token_comp(self,token:str,credentials_exception,db):
      try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         compdata= payload.get("sub")
         user_id=compdata.rsplit("$")[0]
         user_type=compdata.rsplit("$")[1]
         if user_id == None or user_type == "pharmacy":
             raise credentials_exception
         token_data = schemas.TokenData(id=user_id,type=user_type)
      except JWTError:
           raise credentials_exception
      company= comp.Company()
      compa=company.get_company(db=db,company_id=int(token_data.id))   
      if compa== None:
            raise credentials_exception
      return compa
         