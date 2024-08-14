from datetime import datetime, timedelta, timezone
from typing import Annotated
import logging
from dataclasses import dataclass
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.settings import Settings

logger = logging.getLogger(__name__)


@dataclass
class AuthService:
    settings: Settings
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def generate_access_token(self, user_id: str, expires_delta: timedelta | None = None) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        payload = {
            'exp': expire,
            'sub': user_id,
            'iat': datetime.now(timezone.utc)
        }
        encoded_jwt = jwt.encode(payload, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)
        return encoded_jwt
