from datetime import timedelta, datetime
from fastapi import HTTPException, status

import jwt  # Used pyjwt
from settings import (
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES,
    AUTH_SECRET_KEY,
    AUTH_REFRESH_TOKEN_EXPIRE_MINUTES,
    AUTH_HASHING_ALGORITHM
)


class AuthToken:
    """
    Using fastapi-jwt-auth
    https://indominusbyte.github.io/fastapi-jwt-auth/usage/basic/
    """

    @staticmethod
    def generate_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_HASHING_ALGORITHM)

    @staticmethod
    def generate_pair(data: dict) -> dict:
        access_token = AuthToken.generate_access_token(data)
        expire_refresh = datetime.utcnow() + timedelta(minutes=AUTH_REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = jwt.encode(
            {"sub": data.get('sub'), "exp": expire_refresh},
            AUTH_SECRET_KEY,
            algorithm=AUTH_HASHING_ALGORITHM
        )
        return {'access_token': access_token, 'refresh_token': refresh_token}

    @staticmethod
    def decrypt_token(token: str) -> dict:
        if token:
            try:
                # Указываем алгоритмы для декодирования
                encoded = jwt.decode(token, key=AUTH_SECRET_KEY, algorithms=[AUTH_HASHING_ALGORITHM])
                return encoded  # Возвращаем весь декодированный токен
            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"type": "auth.token_expired"},
                )
            except jwt.InvalidTokenError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"type": "auth.token_invalid"},
                )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"type": "auth.token_missing"},
        )
