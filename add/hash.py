from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def verify_password(self,plain_password, hashed_password):
      
        return pwd_context.verify(plain_password, hashed_password)

    def hashing_password (self,password):
        return pwd_context.hash(password)

    def hashing (self,str):
            return pwd_context.hash(str)

    def verify(self,plain, hashed):
          
        return pwd_context.verify(plain, hashed)
        
