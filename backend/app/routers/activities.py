from fastapi import APIRouter

router = APIRouter()


@router.get("/activities")
async def get_activities():
    """TODO: obtener las últimas 10 actividades de escalada del usuario."""
    return {"activities": [], "message": "pendiente de implementar"}