from passlib.context import CryptContext

# We are telling it how hassing algorithm do we want
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash(password:str):
    return pwd_context.hash(password)