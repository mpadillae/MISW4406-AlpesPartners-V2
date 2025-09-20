import httpx
import asyncio
from typing import Dict, Any, Optional
from fastapi import HTTPException
from config import settings


class ServicioAfiliaciones:
    def __init__(self):
        self.base_url = settings.AFILIACIONES_SERVICE_URL
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Realizar petición GET al servicio de afiliaciones"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Realizar petición POST al servicio de afiliaciones"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def close(self):
        """Cerrar cliente HTTP"""
        await self.client.aclose()


class ServicioTracking:
    def __init__(self):
        self.base_url = settings.TRACKING_SERVICE_URL
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Realizar petición GET al servicio de tracking"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Realizar petición POST al servicio de tracking"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def close(self):
        """Cerrar cliente HTTP"""
        await self.client.aclose()


# Instancias globales de los servicios
servicio_afiliaciones = ServicioAfiliaciones()
servicio_tracking = ServicioTracking()
