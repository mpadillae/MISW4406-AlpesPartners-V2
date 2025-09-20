from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any
import os

from api.afiliaciones import router as afiliaciones_router
from api.tracking import router as tracking_router
from config import settings
app_configs: dict[str, Any] = {
    "title": "Alpes Partners BFF",
    "description": "Backend for Frontend - Alpes Partners",
    "version": "1.0.0"
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 BFF iniciando...")
    print(f"📡 Afiliaciones Service: {settings.AFILIACIONES_SERVICE_URL}")
    print(f"📊 Tracking Service: {settings.TRACKING_SERVICE_URL}")

    yield

    print("🛑 BFF cerrando...")

app = FastAPI(lifespan=lifespan, **app_configs)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(afiliaciones_router,
                   prefix="/afiliaciones", tags=["Afiliaciones"])
app.include_router(tracking_router, prefix="/tracking", tags=["Tracking"])


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "bff"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
