print("🔥 SentinelScope backend starting")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import observables, analysis, health
from app.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app FIRST
app = FastAPI(title="SentinelScope")
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"➡️ Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"⬅️ Response status: {response.status_code}")
    return response

# Add middleware AFTER app exists
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, tags=["Health"])
app.include_router(observables.router, prefix="/observables", tags=["Observables"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
