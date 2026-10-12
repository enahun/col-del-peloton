from fastapi import APIRouter, HTTPException, Request

from app.config import settings
from app.services import strava
from app.routers.auth import read_session_cookie

router = APIRouter()


@router.get("/activities")
async def get_activities(request: Request):
    """Devuelve las últimas actividades de escalada del atleta autenticado."""
    cookie = request.cookies.get(settings.session_cookie_name)
    if not cookie:
        raise HTTPException(status_code=401, detail="No autenticado")

    session = read_session_cookie(cookie)
    if not session:
        raise HTTPException(status_code=401, detail="Sesión inválida o expirada")

    access_token = session["access_token"]

    # TODO (siguiente iteración): refrescar token si ha expirado
    # Por ahora Strava devuelve 401 y tocará reloguear.

    try:
        activities = await strava.get_athlete_activities(access_token=access_token, per_page=30)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error con Strava: {e}")

    # Filtrar solo escalada
    climbing = [a for a in activities if a.get("sport_type") == "RockClimbing"]

    # Nos quedamos con las 10 últimas
    return {"count": len(climbing[:10]), "activities": climbing[:10]}