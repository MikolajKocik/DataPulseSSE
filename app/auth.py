import os
from fastapi import HTTPException, Header
from jose import jwt, JWTError

LOCAL_TOKEN = os.getenv("LOCAL_BEARER_TOKEN", "secret_token")
JWT_ISSUER = os.getenv("JWT_ISSUER")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE")
JWT_KEY = os.getenv("JWT_KEY")

def verify_bearer(authorization: str = Header(...)):
    if authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
        # Local token
        if token == LOCAL_TOKEN:
            return True
        # jwt token
        try:
            jwt.decode(
                token,
                JWT_KEY,
                algorithms=["RS256"],
                audience=JWT_AUDIENCE,
                issuer=JWT_ISSUER
            )
            return True
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

