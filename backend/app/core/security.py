import hmac
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import settings

_bearer = HTTPBearer()


def verify_password(plain: str) -> bool:
    # timing-safe comparison prevents brute-force timing attacks
    return hmac.compare_digest(plain, settings.app_password)


def create_access_token() -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.access_token_expire_hours)
    return jwt.encode({"exp": expire}, settings.secret_key, algorithm=settings.algorithm)


def get_current_session(credentials: HTTPAuthorizationCredentials = Depends(_bearer)) -> None:
    try:
        jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")