
import re
from fastapi import HTTPException
from .. import schemas,database
from . import pharmacy,company,dumy,medic
from sqlalchemy.orm import Session

class validate():
    def check_pharamcy(self,pharmacy:schemas.PharmacyCreate,db :Session ): 
        d=dumy.user()
        d.search_user(db=db,busn_id=pharmacy.pha_id,serial=pharmacy.serial,n_id=pharmacy.owner_id)
        self.is_valid_email(pharmacy.email,db=db)    
        self.is_valid_name(pharmacy.username) 
        self.is_valid_phone_number(pharmacy.phone_number,db=db)   
        self.is_valid_Nid(pharmacy.owner_id,db=db)
        self.isvalid_serial(pharmacy.serial,db=db)
        self.isvalid_busn_id(pharmacy.pha_id,db=db )

    def check_company(self,company:schemas.CompanyCreate,db :Session ): 
        d=dumy.user()
        d.search_user(db=db,busn_id=company.comp_id,serial=company.serial,n_id=company.owner_id)
        self.is_valid_email(company.email,db=db)    
        self.is_valid_name(company.username) 
        self.is_valid_phone_number(company.phone_number,db=db)   
        self.is_valid_Nid(company.owner_id,db=db)
        self.isvalid_serial(company.serial,db=db)
        self.isvalid_busn_id(company.comp_id,db=db)

    def check_user(self,user:schemas.userCreate,db:Session):
        self.user_valid_Nid(user.owner_id,db=db)
        self.user_valid_busn_id(user.busn_id,db=db)
        self.user_valid_serial(user.serial,db=db)

    def check_medic(self,medic:schemas.MedicCreate,comp_id:int,db:Session):
        
        self.is_valid_medic(new_medic=medic,comp_id=comp_id,db=db)
        self.is_valid_name(medic.name)
        self.is_valid_name(medic.active_substance)

    def  is_valid_name(self,name :str):
        if all(x.isalpha() or x.isdecimal()  or x.isspace() for x in name):
            pass
        else:
            raise HTTPException(status_code= 400,detail=" name input contain only char " )

    def is_valid_email(self,email:str,db:Session):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            
            p =pharmacy.Pharmacy()
            c =company.Company() 
            e_p=p.get_pharmacy_by_email(email=email,db=db)
            e_c=c.get_company_by_email(email=email,db=db)
            if(e_p or e_c ):
                 raise HTTPException(status_code=400, detail=" This Email is Already Used ")
           
        else:
            raise HTTPException(status_code=400, detail=" invalid form for email ")

    def is_valid_Nid(self,nid:str,db:Session):
        if(len(nid)==14):
            if(nid.isdecimal()):
                u=dumy.user()
                p=pharmacy.Pharmacy()
                c=company.Company()
                n_p=p.get_pharmacy_by_owner_id(owner_id=nid,db=db)
                n_c=c.get_company_by_owner_id(owner_id=nid,db=db)
                if(n_p or n_c):
                    raise  HTTPException(status_code=400, detail="  This OwnerID is Already Used  ")   


            else:
             raise  HTTPException(status_code=400, detail="  National ID is only contain decimal digits ")   
        else:
            raise  HTTPException(status_code=400, detail="  National ID length not equal 14 ")   

    def is_valid_phone_number(self,phone_number:str,db:Session):
        if(phone_number.isdecimal()):
            if(len(phone_number)== 11):
               
                p=pharmacy.Pharmacy()
                c=company.Company()
                pn_p=p.get_pharmacy_by_phone_number(phone_number=phone_number,db=db)
                cn_c=c.get_company_by_phoen_number(phone_number=phone_number,db=db)
                if(pn_p or cn_c ):
                    raise  HTTPException(status_code=400, detail=   "  This Phone number is alrady used ")   
            else:
                raise  HTTPException(status_code=400, detail="  Phone Number length not equal 11 ")   

        else:
            raise  HTTPException(status_code=400, detail=" invalid form for Phone Number")   

    def isvalid_serial(self,serial:str,db:Session):
        if(serial.isdecimal() ):
            if(len(serial)== 6):
               p=pharmacy.Pharmacy()
               c=company.Company()
               s_p=p.get_pharmacy_by_serial(serial=serial,db=db)
               s_c=c.get_company_by_serial(serial=serial,db=db)
               if(s_p or s_c):
                raise  HTTPException(status_code=400, detail=" this serial is alrady Used ")   

            else:
                raise  HTTPException(status_code=400, detail="  serial length not equal 6 ")   

        else:
            raise  HTTPException(status_code=400, detail=" invalid form for serial only contain number")   
               
    def isvalid_busn_id(self,busn_id:str,db:Session):
        if(busn_id.isdecimal() ):
            if(len(busn_id)== 6):
               p=pharmacy.Pharmacy()
               c=company.Company()
               s_p=p.get_pharmacy_by_pha_id(pha_id=busn_id,db=db)
               s_c=c.get_company_by_comp_id(comp_id=busn_id,db=db)
               if(s_p or s_c):
                raise  HTTPException(status_code=400, detail=" this Id is alrady Used ")   

            else:
                raise  HTTPException(status_code=400, detail="  Id length not equal 6 ")   

        else:
            raise  HTTPException(status_code=400, detail=" invalid form for serial only contain number")   

    def user_valid_busn_id(self,busn_id:str,db:Session):
        if(busn_id.isdecimal() ):
            if(len(busn_id)== 6):
                 u=dumy.user()
                 b_u=u.get_user_by_busn_id(busn_id=busn_id,db=db)
                 if(b_u):
                     raise  HTTPException(status_code=400, detail=" this Bussnes Id Is Alrady Used ")   
            else:
                raise  HTTPException(status_code=400, detail="  Id length not equal 6 ")   

        else:
            raise  HTTPException(status_code=400, detail=" invalid form for serial only contain number")   

    def user_valid_serial(self,serial:str,db:Session):
        if(serial.isdecimal() ):
            if(len(serial)== 6):
                u=dumy.user()
                u_s=u.get_user_by_serial(serial=serial,db=db)
                if(u_s):
                    raise HTTPException(status_code=400,detail="this serial is already used")
            else:
                raise  HTTPException(status_code=400, detail="  serial length not equal 6 ")   

        else:
            raise  HTTPException(status_code=400, detail=" invalid form for serial only contain number")   
 
    def  user_valid_Nid(self,nid:str,db:Session):
        if(len(nid)==14):
            if(nid.isdecimal()):
                u=dumy.user()
                u_n=u.get_user_by_n_id(db=db,n_id=nid)
                if(u_n):
                    raise HTTPException(status_code=400,detail="This National ID Is alrady Used")
                
            else:
             raise  HTTPException(status_code=400, detail="  National ID is only contain decimal digits ")   
        else:
            raise  HTTPException(status_code=400, detail="  National ID length not equal 14 ")   

    def is_log_valid_email(self,email:str):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            pass  
        else:
            raise HTTPException(status_code=400, detail=" invalid form for email ")

    def is_valid_medic(self,new_medic:schemas.MedicCreate,comp_id:int,db:Session):
        m=medic.Medic()
        c_m=m.check_medic(db=db,medic=new_medic,comp_id=comp_id)
        if(c_m ):
            raise HTTPException(status_code=400 , detail=" this medic is alrady exist")