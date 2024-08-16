from datetime import datetime, timedelta, timezone
from typing import Annotated
import logging
from dataclasses import dataclass
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.exception import TokenNotCorrectException, TokenExpireExtension
from app.core.settings import Settings

logger = logging.getLogger(__name__)


@dataclass
class AuthService:
    settings: Settings
    # Todo: url подкорректировать.
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def generate_access_token(self, user_id: str, expires_delta: timedelta | None = None) -> str:
        # Можно указать свою expires_delta=timedelta(hours=2).
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        payload = {
            'expire': expire,
            'sub': user_id,
            'iat': datetime.now(timezone.utc)
        }
        encoded_jwt = jwt.encode(payload, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)
        return encoded_jwt

    def get_user_id_from_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except InvalidTokenError:
            raise TokenNotCorrectException
        if payload['expire'] < datetime.now().timestamp():
            raise TokenExpireExtension
        return payload['user_id']

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
