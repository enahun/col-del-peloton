from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, activities

app = FastAPI(
    title="Col del Pelotón API",
    description="API para el dashboard de escalada conectado a Strava",
    version="0.1.0",
)

# CORS: permitimos que el frontend (Vercel o localhost) nos llame
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(activities.router, prefix="/api", tags=["activities"])


@app.get("/")
async def root():
    return {"status": "ok", "service": "Col del Pelotón API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}