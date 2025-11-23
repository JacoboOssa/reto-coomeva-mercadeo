"""
FastAPI application for clustering predictions using UMAP + KMeans
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.routes import clustering

app = FastAPI(
    title="Coomeva Clustering API",
    description="API para clusterizar usuarios usando UMAP + KMeans",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clustering.router, prefix="/api/v1", tags=["clustering"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Coomeva Clustering API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "models_loaded": True
    }


# AWS Lambda handler
handler = Mangum(app, lifespan="off")
