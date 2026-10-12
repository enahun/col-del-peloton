from pydantic import BaseModel


class ClimbActivity(BaseModel):
    id: int
    name: str
    sport_type: str
    start_date: str
    moving_time: int          # segundos
    elapsed_time: int         # segundos
    total_elevation_gain: float
    distance: float | None = None
    average_heartrate: float | None = None
    max_heartrate: float | None = None