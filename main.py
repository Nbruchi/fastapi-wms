from fastapi import FastAPI
from app.api.waste_types import waste_types_router
from app.api.collection_points import collection_points_router
from app.api.collection_schedules import collection_schedules_router
from app.api.collection_records import collection_records_router
from app.api.users import users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(waste_types_router)
app.include_router(collection_points_router)
app.include_router(collection_schedules_router)
app.include_router(collection_records_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)