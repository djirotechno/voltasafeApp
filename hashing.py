from passlib.context import CryptContext
pw_cxt = CryptContext(schemes=["bcrypt"],deprecated = "auto")

class Hash():
    def bcrypt(password:str):
        return  pw_cxt.hash(password)
    
    def verifie(hashed_password,plain_password):
        
        return pw_cxt.verify(plain_password,hashed_password)
        
    

