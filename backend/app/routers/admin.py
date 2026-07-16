from fastapi import APIRouter, Depends

from app.admin_auth import require_admin

router = APIRouter(prefix="/admin")


@router.get("/me")
def get_me(claims: dict = Depends(require_admin)) -> dict:
    return {"email": claims.get("email"), "uid": claims.get("uid")}
