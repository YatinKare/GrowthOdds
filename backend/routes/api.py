from fastapi import APIRouter
from routes.health import router as health_router
from routes.experiment import router as experiment_router

api_router = APIRouter()

# Register all sub-routers here
api_router.include_router(health_router, prefix="/system", tags=["health"])
api_router.include_router(experiment_router, prefix="/experiment", tags=["experiments"])
