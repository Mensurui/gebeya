import jwt
from fastapi.security import OAuth2PasswordBearer
from ..data.dependency import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from . import schema
from ..model import model
from sqlalchemy.future import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 30

def create_access_token(data):
    to_encode = jsonable_encoder(data)
    print(f"To Encode {to_encode}")
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id = id)
        print(f"Token Data {token_data}")
    except InvalidTokenError:
        raise credentials_exception

    return token_data

async def get_admin(token:str=Depends(oauth2_scheme), db:AsyncSession=Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user_query = await db.execute(select(model.Admin).where(model.Admin.username == token.id))
    user = user_query.scalars().first()
    print(f"User is: {user}")
    if user is None:
        raise credentials_exception
    return user.username
