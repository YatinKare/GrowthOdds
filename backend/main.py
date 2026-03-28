from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.api import api_router
from db.session import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database and tables on startup
    create_db_and_tables()
    yield

app = FastAPI(title="GrowthOdds API", lifespan=lifespan)

# Include the main API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to GrowthOdds API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
