from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from sql_app.database import SessionLocal, engine,get_db


oauth2_company_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_pharmacy_scheme = OAuth2PasswordBearer(tokenUrl="login")
from . import token
tok =token.tok()

async def get_current_pharmacy_or_company(token: str = Depends(oauth2_pharmacy_scheme),db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user=tok.verify_token_pha_or_comp(token=token,credentials_exception=credentials_exception,db=db)
    return user


async def get_current_pharmacy(token: str = Depends(oauth2_pharmacy_scheme),db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    pha=tok.verify_token_pha(token=token,credentials_exception=credentials_exception,db=db)
    return pha
    
async def get_current_company(token: str = Depends(oauth2_company_scheme),db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
     )
    pha=tok.verify_token_comp(token=token,credentials_exception=credentials_exception,db=db)
    return pha
   