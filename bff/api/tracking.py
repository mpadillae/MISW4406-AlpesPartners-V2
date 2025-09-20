from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import uuid
from pydantic import BaseModel

from servicios import servicio_tracking

router = APIRouter()

# DTOs


class EventoTrackingRequest(BaseModel):
    id_campana: uuid.UUID
    tipo_evento: str
    datos: Dict[str, Any]


class MetricasResponse(BaseModel):
    id: uuid.UUID
    id_campana: uuid.UUID
    id_marca: uuid.UUID
    nombre_campana: str
    estado: str
    fecha_creacion: str
    fecha_inicio: str = None
    presupuesto: float
    metricas: Dict[str, Any]


class EventoTrackingResponse(BaseModel):
    id: uuid.UUID
    id_campana: uuid.UUID
    tipo_evento: str
    datos: Dict[str, Any]
    fecha_evento: str

# Endpoints


@router.post("/evento")
async def registrar_evento_tracking(request: EventoTrackingRequest):
    """Registrar un evento de tracking"""
    try:
        # Convertir UUIDs a strings para la serialización JSON
        data = request.dict()
        if 'id_campana' in data:
            data['id_campana'] = str(data['id_campana'])
        response = await servicio_tracking.post("/tracking/evento", data)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metricas/{id_campana}")
async def obtener_metricas_campana(id_campana: uuid.UUID):
    """Obtener métricas de una campaña"""
    try:
        response = await servicio_tracking.get(f"/tracking/metricas/{str(id_campana)}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/eventos/{id_campana}")
async def obtener_eventos_campana(id_campana: uuid.UUID):
    """Obtener eventos de una campaña"""
    try:
        response = await servicio_tracking.get(f"/tracking/eventos/{str(id_campana)}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metricas/marca/{id_marca}")
async def obtener_metricas_por_marca(id_marca: uuid.UUID):
    """Obtener métricas por marca"""
    try:
        response = await servicio_tracking.get(f"/tracking/metricas/marca/{str(id_marca)}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
