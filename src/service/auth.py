from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter
from ..data.dependency import get_db
from sqlalchemy.future import select
from .utils import verify_password
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .oauth2 import create_access_token
from ..model import model
from . import schema, utils, oauth2
from fastapi.encoders import jsonable_encoder
router = APIRouter()

@router.post('/login', response_model=schema.Token)
async def admin_login(admin_credentials:OAuth2PasswordRequestForm=Depends(), db:AsyncSession=Depends(get_db)):
    admin_query = await db.execute(select(model.Admin).where(model.Admin.username == admin_credentials.username))
    admin_result = admin_query.scalar()
    if not admin_result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify_password(admin_credentials.password, admin_result.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"id":admin_result.username})
    return {"access_token":access_token, "token_type":"bearer"}
