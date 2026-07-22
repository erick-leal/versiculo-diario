from fastapi import Header, HTTPException

from app.core.config import settings
from app.firebase_verify import verify_firebase_token


def require_admin(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Falta el token de administrador")

    token = authorization.removeprefix("Bearer ")
    try:
        claims = verify_firebase_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    # verify_firebase_token solo confirma que el token es un ID token valido de
    # ESTE proyecto de Firebase, no que sea el admin - cualquiera puede
    # autoregistrarse (Email/Password esta habilitado para que el admin real
    # inicie sesion), asi que la unica cuenta autorizada se valida aqui.
    if claims.get("email") != settings.admin_email:
        raise HTTPException(status_code=403, detail="No autorizado")

    return claims
