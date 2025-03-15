import jwt
from . import schemas
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . config import Settings

oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")



def create_access_token(data: dict):
    data_to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(Settings.TOKEN_EXPIRE_MINUTES))
    data_to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(data_to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])

        id = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data
def get_current_user(token: str = Depends(oauth2scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, credentials_exception)    
