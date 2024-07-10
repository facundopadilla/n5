from fastapi import APIRouter

from src.routes.v1.login import router as login_router
from src.routes.v1.people import router as people_router
from src.routes.v1.vehicles import router as vehicles_router
from src.routes.v1.police_officers import router as police_officers_router
from src.routes.v1.traffic_violations import router as traffic_violations_router

base_v1 = APIRouter(prefix="/api/v1")
base_v1.include_router(login_router)
base_v1.include_router(people_router)
base_v1.include_router(vehicles_router)
base_v1.include_router(police_officers_router)
base_v1.include_router(traffic_violations_router)
