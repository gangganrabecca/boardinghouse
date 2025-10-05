from fastapi import FastAPI
from app.routes import auth, boarding_house
from app.database.neo4j_connector import neo4j_connector
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    neo4j_connector.connect()
    yield
    # Shutdown
    neo4j_connector.close()

app = FastAPI(
    title="Boarding House Management API",
    description="A complete backend system for managing boarding houses",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(auth.router)
app.include_router(boarding_house.router)

@app.get("/")
async def root():
    return {"message": "Boarding House Management API", "status": "running"}

@app.get("/health")
async def health_check():
    try:
        with neo4j_connector.get_session() as session:
            session.run("RETURN 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)