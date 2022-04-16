import string as s
import random


s2=list(s.ascii_uppercase)
s3=list(s.digits)

characters_number=6

# ------------------------ get random code  contain upercase letters and digits---------------------------

def get_auth_code():
    random.shuffle(s2)
    random.shuffle(s3)
    
    password=[]
    for i in range(4):
        password.append(s2[i])
    for i in range(2):
        password.append(s3[i])
    random.shuffle(password)
    password="".join(password[:])
    return password

